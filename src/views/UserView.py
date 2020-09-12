#/src/views/UserView

from flask import request, json, Response, Blueprint, g
from ..models.UserModel import UserModel, UserSchema
from ..shared.Authentication import Auth
import os
import requests
import random
import datetime


user_api = Blueprint('user_api', __name__)
user_schema = UserSchema()

@user_api.route('/', methods=['GET'])
def get_all():
  """
  Get all users
  """
  users = UserModel.get_all_users()
  ser_users = user_schema.dump(users, many=True)
  print(ser_users)
  return custom_response(ser_users, 200)


@user_api.route('/signup', methods=['POST'])
def create():
  """
  Create User Function
  """
  req_data = request.get_json()
#   print(req_data)
  data, error = user_schema.load(req_data)

  if error:
    return custom_response(error, 400)
  
  # check if user already exist in the db
  user_in_db = UserModel.get_user_by_email(data.get('email'))
  if user_in_db:
    message = {'error': 'User already exist, please supply another email address'}
    return custom_response(message, 400)

  user = UserModel(data)
  user.save()
  print(data, user)
  ser_data = user_schema.dump(user)
  return(custom_response(ser_data, 200))

@user_api.route('/<string:username>/zoom_login', methods=['POST'])
def store_zoom_token(username):
  """
  takes the authcode, fetches the proper bearer token, and stores the token
  in the user table.
  """
  user = UserModel.get_user_by_name(username)
  to_update = user_schema.dump(user)
  auth_code = request.get_json()['auth_code']
  hdrs = {"Authorization": "Basic " + os.getenv('ENCODED_ID_SECRET')}
  resp = requests.post('https://zoom.us/oauth/token?grant_type=authorization_code&code='+auth_code+'&redirect_uri=https://www.roomy-pennapps.space/home', headers=hdrs)
  b_token = resp.json().get("access_token")
  if resp.status_code != 200:
      return custom_response("failed to get bearer from zoom", 500)
  user.update({"zoom_token": b_token, "last_login": datetime.datetime.utcnow(), "online":True})
  new_u = user_schema.dump(user)
  return custom_response(new_u, 200)





# @user_api.route('/', methods=['POST'])
# def create():
#   """
#   Create User Function
#   """
#   req_data = request.get_json()
#   data, error = user_schema.load(req_data)

#   if error:
#     return custom_response(error, 400)
  
#   # check if user already exist in the db
#   user_in_db = UserModel.get_user_by_email(data.get('email'))
#   if user_in_db:
#     message = {'error': 'User already exist, please supply another email address'}
#     return custom_response(message, 400)
  
#   user = UserModel(data)
#   user.save()
#   ser_data = user_schema.dump(user).data
#   token = Auth.generate_token(ser_data.get('id'))
#   return custom_response({'jwt_token': token}, 201)

# @user_api.route('/<int:user_id>', methods=['GET'])
# def get_a_user(user_id):
#   """
#   Get a single user
#   """
#   user = UserModel.get_one_user(user_id)
#   if not user:
#     return custom_response({'error': 'user not found'}, 404)
  
#   ser_user = user_schema.dump(user).data
#   return custom_response(ser_user, 200)

# @user_api.route('/me', methods=['PUT'])
# # @Auth.auth_required
# def update():
#   """
#   Update me
#   """
#   req_data = request.get_json()
#   data, error = user_schema.load(req_data, partial=True)
#   if error:
#     return custom_response(error, 400)

#   user = UserModel.get_one_user(g.user.get('id'))
#   user.update(data)
#   ser_user = user_schema.dump(user).data
#   return custom_response(ser_user, 200)

# @user_api.route('/me', methods=['DELETE'])
# # @Auth.auth_required
# def delete():
#   """
#   Delete a user
#   """
#   user = UserModel.get_one_user(g.user.get('id'))
#   user.delete()
#   return custom_response({'message': 'deleted'}, 204)

# @user_api.route('/me', methods=['GET'])
# # @Auth.auth_required
# def get_me():
#   """
#   Get me
#   """
#   user = UserModel.get_one_user(g.user.get('id'))
#   ser_user = user_schema.dump(user).data
#   return custom_response(ser_user, 200)


# @user_api.route('/login', methods=['POST'])
# def login():
#   """
#   User Login Function
#   """
#   req_data = request.get_json()

#   data, error = user_schema.load(req_data, partial=True)
#   if error:
#     return custom_response(error, 400)
#   if not data.get('email') or not data.get('password'):
#     return custom_response({'error': 'you need email and password to sign in'}, 400)
#   user = UserModel.get_user_by_email(data.get('email'))
#   if not user:
#     return custom_response({'error': 'invalid credentials'}, 400)
#   if not user.check_hash(data.get('password')):
#     return custom_response({'error': 'invalid credentials'}, 400)
#   ser_data = user_schema.dump(user).data
#   token = Auth.generate_token(ser_data.get('id'))
#   return custom_response({'jwt_token': token}, 200)

  

def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )
