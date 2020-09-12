#/src/views/UserView

from flask import request, json, Response, Blueprint, g
from ..models.UserModel import UserModel, UserSchema
from ..models.BigRoomModel import BigRoomModel, BigRoomSchema
from ..models.GymModel import GymModel, GymSchema
from ..shared.Authentication import Auth
import datetime
import requests
import json

gym_api = Blueprint('gym_api', __name__)
user_schema = UserSchema()
br_schema = BigRoomSchema()
gym_schema = GymSchema()


@gym_api.route('/', methods=['GET'])
def get_all():
  """
  Get all gyms
  """
  gym = GymModel.get_all_gyms()
  gyms = gym_schema.dump(gym, many=True)
  print(gyms)
  return custom_response(gyms, 200)

@gym_api.route('/<int:gym_id>', methods=['GET'])
def get_a_gym(gym_id):
  """
  Get a single user
  """
  gym = GymModel.get_one_gym(gym_id)
  if not gym:
    return custom_response({'error': 'gym not found'}, 404)
  
  gymr = gym_schema.dump(gym)
  return custom_response(gymr, 200)

@gym_api.route('/join/<int:gym_id>', methods=['PUT'])
def add_a_user(gym_id):
  """
  adds a single user into the gym
  """
  user_id = request.get_json()['user_id']
  user = UserModel.get_one_user(user_id)
  if not user:
    return custom_response({'error': 'user not found'}, 404)
  print(user.name)
  g = GymModel.get_one_gym(gym_id)
  new_mems = list(g.activemembers)
  if user_id not in new_mems: new_mems.append(user_id)
  g.update({"active": new_mems})
  newg = gym_schema.dump(g)
  return custom_response(newg, 200)
  
@gym_api.route('/<int:g_id>', methods=['GET'])
def get_one(g_id):
  """
  Get specific br data
  """
  br = GymModel.get_one_gym(g_id)
  rm = gym_schema.dump(br)
  return custom_response(rm, 200)

# for tim to poll to see whos active
@gym_api.route('/<int:g_id>/whos_active', methods=['GET'])
def get_br_members(g_id):
    return custom_response(GymModel.get_one_gym(g_id).active, 200)

# lets a person join the big room and updates db
@gym_api.route('/<int:br_id>/joined_gym', methods=['PUT'])
def joining_member(br_id):
    new = request.get_json()['username']
    br = GymModel.get_one_gym(br_id)
    new_mems = list(br.active)
    # if empty, start a meeting
    if not new_mems:
        start_zoom_meeting(request.get_json()['id'])
    if new not in new_mems:
        new_mems.append(new)
    br.update({"active" : new_mems})
    return custom_response(new_mems, 200)

# for tim to signal when someone leaves, and updates db
@gym_api.route('/<int:br_id>/left_gym', methods=['PUT'])
def signal_leaving_member(br_id):
    leaving = request.get_json()['username']
    br = GymModel.get_one_gym(br_id)
    new_mems = [mem for mem in br.active if mem != leaving]
    br.update({"active" : new_mems})
    return custom_response(new_mems, 200)


def start_zoom_meeting(id):
    usr = UserModel.get_one_user(id)
    token = usr.zoom_token
    body = {"topic": "workout",
    "start_time": str(datetime.datetime.utcnow()),
    "duration": 30,
    "timezone": "America/Los_Angeles",
    "agenda": "Working Out",
    "settings": {
        "host_video": "true",
        "participant_video": "true",
        "join_before_host": "true"
    }
    }
    print("here\n",token)
    print(json.dumps(body))
    resp = requests.post('https://api.zoom.us/v2/users/'+usr.user_id+'/meetings', json = body, headers = {"Content-Type":"application/json","Authorization" : "Bearer "+ token, "Connection":"keep-alive"})
    print("post stuff", resp.content)
    print(resp.json())
    return custom_response(resp.json(), 200)
    





def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )
