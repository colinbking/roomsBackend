#/src/views/UserView

from flask import request, json, Response, Blueprint, g
from ..models.UserModel import UserModel, UserSchema
from ..models.BigRoomModel import BigRoomModel, BigRoomSchema
from ..models.GymModel import GymModel, GymSchema
from ..models.CafeModel import CafeModel, CafeSchema

from ..shared.Authentication import Auth
import datetime
import requests
import json

cafe_api = Blueprint('cafe_api', __name__)
user_schema = UserSchema()
br_schema = BigRoomSchema()
cafe_schema = CafeSchema()



@cafe_api.route('/', methods=['GET'])
def get_all():
  """
  Get all gyms
  """
  cafe = CafeModel.get_all_cafes()
  cafes = cafe_schema.dump(cafe, many=True)
  return custom_response(cafes, 200)

@cafe_api.route('/<int:cafe_id>', methods=['GET'])
def get_a_gym(cafe_id):
  """
  Get a single cafe
  """
  cafe = CafeModel.get_one_cafe(cafe_id)
  if not cafe:
    return custom_response({'error': 'cafe not found'}, 404)
  
  cafer = cafe_schema.dump(cafe)
  return custom_response(cafer, 200)
  
@cafe_api.route('/<int:cafe_id>', methods=['GET'])
def get_one(cafe_id):
  """
  Get specific br data
  """
  cafe = CafeModel.get_one_cafe(cafe_id)
  rm = cafe_schema.dump(cafe)
  return custom_response(rm, 200)

# for tim to poll to see whos active
@cafe_api.route('/<int:cafe_id>/whos_active', methods=['GET'])
def get_br_members(cafe_id):
    return custom_response(CafeModel.get_one_cafe(cafe_id).active, 200)

# lets a person join the big room and updates db
@cafe_api.route('/<int:cafe_id>/joined_cafe', methods=['PUT'])
def joining_member(cafe_id):
    new = request.get_json()['username']
    cafe = CafeModel.get_one_cafe(cafe_id)
    new_mems = list(cafe.active)
    # if empty, start a meeting
    new_meeting = cafe.zoom_mtg
    if not new_mems or not new_meeting:
        new_meeting = start_zoom_meeting(request.get_json()['id'])["join_url"]
        cafe.update({"active" : new_mems, "zoom_mtg": new_meeting})
    if new not in new_mems:
        new_mems.append(new)
    return custom_response({"active_members" : new_mems, "meeting" : new_meeting}, 200)

# for tim to signal when someone leaves, and updates db
@cafe_api.route('/<int:cafe_id>/left_cafe', methods=['PUT'])
def signal_leaving_member(cafe_id):
    leaving = request.get_json()['username']
    g = CafeModel.get_one_cafe(cafe_id)
    new_mems = [mem for mem in g.active if mem != leaving]
    g.update({"active" : new_mems})
    # clean up youtube and zom meeting if last person
    if not new_mems or not g.active:
        g.update({"video_started":None, "zoom_mtg":None})
    return custom_response(new_mems, 200)

# for tim to signal when someone starts workout
@cafe_api.route('/<int:cafe_id>/video', methods=['GET'])
def start_workout(cafe_id):
    start_t = datetime.datetime.utcnow()
    g = CafeModel.get_one_cafe(cafe_id)
    # store timestamp in db
    started = g.video_started
    if not started:
        g.update({"video_started" : start_t})
        return custom_response({"time" : 0}, 200)
    else:
        diff = (datetime.datetime.utcnow() - started).total_seconds()
        return custom_response({'time': int(diff)}, 200)


# for tim to signal when someone starts workout
@cafe_api.route('/<int:c_id>/set_note', methods=['POST'])
def set_note(c_ud):
    note = request.get_json()['note']
    g = CafeModel.get_one_cafe(c_id)
    g.update({"note": note})
    return custom_response({"note":note}, 200)


def start_zoom_meeting(id):
    usr = UserModel.get_one_user(id)
    token = usr.zoom_token
    body = {"topic": "workout",
    "start_time": str(datetime.datetime.utcnow()),
    "duration": 30,
    "timezone": "America/Los_Angeles",
    "agenda": "Cafe Chilling",
    "settings": {
        "host_video": "true",
        "participant_video": "true",
        "join_before_host": "true"
    }
    }

    resp = requests.post('https://api.zoom.us/v2/users/'+usr.email+'/meetings', json = body, headers = {"Content-Type":"application/json","Authorization" : "Bearer "+ token, "Connection":"keep-alive"})
    return resp.json()
    





def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )
