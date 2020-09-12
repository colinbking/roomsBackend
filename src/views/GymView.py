#/src/views/UserView

from flask import request, json, Response, Blueprint, g
from ..models.UserModel import UserModel, UserSchema
from ..models.BigRoomModel import BigRoomModel, BigRoomSchema
from ..models.GymModel import GymModel, GymSchema

from ..shared.Authentication import Auth

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
    return custom_response({'error': 'user not found'}, 404)
  
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
  g.update({"activemembers": new_mems})
  newg = gym_schema.dump(g)

  return custom_response(newg, 200)

# @gym_api.route('/', methods=['POST'])
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


# @gym_api.route('/me', methods=['PUT'])
# # @Auth.auth_required
# def update():
#   """ppython
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

# @gym_api.route('/me', methods=['DELETE'])
# # @Auth.auth_required
# def delete():
#   """
#   Delete a user
#   """
#   user = UserModel.get_one_user(g.user.get('id'))
#   user.delete()
#   return custom_response({'message': 'deleted'}, 204)

# @gym_api.route('/me', methods=['GET'])
# # @Auth.auth_required
# def get_me():
#   """
#   Get me
#   """
#   user = UserModel.get_one_user(g.user.get('id'))
#   ser_user = user_schema.dump(user).data
#   return custom_response(ser_user, 200)


# @gym_api.route('/login', methods=['POST'])
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
