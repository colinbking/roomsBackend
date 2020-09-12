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


def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )
