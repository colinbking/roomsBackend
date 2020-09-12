#/src/views/UserView

from flask import request, json, Response, Blueprint, g
from ..models.UserModel import UserModel, UserSchema
from ..models.BigRoomModel import BigRoomModel, BigRoomSchema
from ..shared.Authentication import Auth

br_api = Blueprint('br_api', __name__)
user_schema = UserSchema()
br_schema = BigRoomSchema()

@br_api.route('/', methods=['GET'])
def get_all():
  """
  Get all bigrooms
  """
  br = BigRoomModel.get_all_big_rooms()
  rms = br_schema.dump(br, many=True)
  print(rms)
  return custom_response(rms, 200)

@br_api.route('/<int:br_id>', methods=['GET'])
def get_one(br_id):
  """
  Get specific br data
  """
  br = BigRoomModel.get_one_big_room(br_id)
  rm = br_schema.dump(br)
  return custom_response(rm, 200)

# for tim to poll to see whos active
@br_api.route('/<int:br_id>/whos_active', methods=['GET'])
def get_br_members(br_id):
    return custom_response(BigRoomModel.get_one_big_room(br_id).active, 200)

# lets a person join the big room and updates db
@br_api.route('/<int:br_id>/joined_br', methods=['POST'])
def joining_member(br_id):
    new = request.get_json()['username']
    br = BigRoomModel.get_one_big_room(br_id)
    new_mems = list(brm.active)
    if new not in new_mems:
        new_mems.append(new)
    br.update({"active" : new_mems})
    return custom_response(new_mems, 200)

# for tim to signal when someone leaves, and updates db
@br_api.route('/<int:br_id>/left_br', methods=['POST'])
def signal_leaving_member(br_id):
    leaving = request.get_json()['username']
    br = BigRoomModel.get_one_big_room(br_id)
    brm = br_schema.dump(br)
    new_mems = [mem for mem in brm.active if mem != leaving]
    br.update({"active" : new_mems})
    return custom_response(new_mems, 200)



def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )
