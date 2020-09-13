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
  # print(ser_users)
  return custom_response(ser_users, 200)


@user_api.route('/signup', methods=['POST'])
def create():
  """
  Create User Function
  """
  req_data = request.get_json()
  name = req_data.get('username')
  email = req_data.get('email')
  new_user = UserModel(id= random.randint(5,10000000), username = name, email=email)
#   print(req_data)

  
  # check if user already exist in the db
  user_in_db = UserModel.get_user_by_name(new_user.username)
  if user_in_db:
    message = {'error': 'User already exist, please supply another username'}
    return custom_response(message, 400)

  new_user.save()
  ser_data = user_schema.dump(new_user)
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




import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import spotipy.util as util
# import pprint
import requests

# pp = pprint.PrettyPrinter()

# @user_api.route('/callback/<string:authtoken>', methods=['GET'])
# def extractAuthToken(authtoken):
#   # authtoken = authtoken.split("?code=")[0]
#   authtoken = "https://papps2020.uc.r.appspot.com/user/callback/" + authtoken

#   print("authtoken is = ", authtoken)
#   import sys
#   from io import StringIO

#   sys.stdin = StringIO(authtoken)

#   return custom_response({"result":"success"}, 200)

@user_api.route('/<string:username>/get_spotify_info', methods=['GET'])
def get_new_spotify_playlist(username):
  """
  
  """
  user = UserModel.get_user_by_name(username)

  # # delete .cache
  # import os
  # APP_ROOT = os.path.dirname(os.path.abspath(__file__))
  # APP_ROOT = APP_ROOT[:-9]
  # if os.path.isfile('.cache'):
  #   os.remove(os.path.join(APP_ROOT, '.cache'))
  #   print(APP_ROOT)




  # Start Oauth2

  # auth_manager = SpotifyClientCredentials()
  # sp = spotipy.Spotify(auth_manager=auth_manager)


  # export SPOTIPY_CLIENT_ID='eae14429b373461aadc72104110154f9'
  # export SPOTIPY_CLIENT_SECRET='ada7bc6d1a1d4eada84cf382ae26c4f0'

  # username = '31a4izbs5mkyksxuhdzetwyoivfm'
  scope = "user-read-recently-played playlist-modify-public user-library-modify playlist-read-collaborative playlist-modify-private"
  redirect_uri = "https://www.roomy-pennapps.space/home/"
  # redirect_uri = "http://localhost:8080/"
  # redirect_uri = "https://papps2020.uc.r.appspot.com/user/callback/"
  # redirect_uri = "http://example.com/callback/"

  # username = 'shjang956'
  # token = util.prompt_for_user_token(username, scope, client_id ="eae14429b373461aadc72104110154f9", client_secret = "ada7bc6d1a1d4eada84cf382ae26c4f0", redirect_uri='https://www.roomy-pennapps.space/home/')
  token = True
  if token:

    sp_auth = SpotifyOAuth(client_id="eae14429b373461aadc72104110154f9",
                                                  client_secret="ada7bc6d1a1d4eada84cf382ae26c4f0",
                                                  redirect_uri=redirect_uri,
                                                  scope=scope)                                          
    sp = spotipy.Spotify(auth_manager=sp_auth)

    # sp = spotipy.Spotify(auth=token)


    # url = sp_auth.get_authorize_url()
    # print(url)

  else:
    # print("Can't get token for ", username)
    print("Error getting token")

  

  # # Get recently played song from the user, and get the artist name and artist id

  results = sp.current_user_recently_played()
  # print(results)
  print(sp.current_user())

  for idx, item in enumerate(results['items']):
      track = item['track']
      artist_id = track['artists'][0]['id']
      artist_name = track['artists'][0]['name']
      # pp.pprint(track)
      # print(artist_name, artist_id)
      break


  

  # now get artist info and extract genre


  resp = requests.get('https://api.spotify.com/v1/artists/' + artist_id, headers = {'Authorization': '{} {}'.format(sp.auth_manager.get_cached_token()['token_type'], sp.auth_manager.get_cached_token()['access_token'])})
  if resp.status_code != 200:
      print("ERROR!")

  genres = resp.json()['genres']
  # print(genres)

  user.update({"genres":genres, "artist":artist_id})


  return custom_response({"result": "good"}, 200)







@user_api.route('/add_playlist/gym/<string:username>', methods=['GET'])
def add_gym_playlist(username):
  user = UserModel.get_user_by_name(username)

  artist_id = user.artist_id
  genres = user.genres


  scope = "user-read-recently-played playlist-modify-public user-library-modify playlist-read-collaborative playlist-modify-private"
  redirect_uri = "https://www.roomy-pennapps.space/home/"
  # redirect_uri = "http://localhost:8080/"
  # redirect_uri = "https://papps2020.uc.r.appspot.com/user/callback/"
  # redirect_uri = "http://example.com/callback/"

  # username = 'shjang956'
  # token = util.prompt_for_user_token(username, scope, client_id ="eae14429b373461aadc72104110154f9", client_secret = "ada7bc6d1a1d4eada84cf382ae26c4f0", redirect_uri='https://www.roomy-pennapps.space/home/')
  token = True
  if token:

    sp_auth = SpotifyOAuth(client_id="eae14429b373461aadc72104110154f9",
                                                  client_secret="ada7bc6d1a1d4eada84cf382ae26c4f0",
                                                  redirect_uri=redirect_uri,
                                                  scope=scope)                                          
    sp = spotipy.Spotify(auth_manager=sp_auth)

    # sp = spotipy.Spotify(auth=token)


    # url = sp_auth.get_authorize_url()
    # print(url)

  else:
    # print("Can't get token for ", username)
    print("Error getting token")




  # artist_id, genres

  # Get random new songs from seeds (genre and artist)

  resp = requests.get('https://api.spotify.com/v1/recommendations/?market={}&seed_artists={}&seed_genres={}&min_energy={}&min_popularity={}'.format(
      'US', artist_id, ','.join(genres[:5]), 0.4, 50
  ),  headers = {'Authorization': '{} {}'.format(sp.auth_manager.get_cached_token()['token_type'], sp.auth_manager.get_cached_token()['access_token'])})
  if resp.status_code != 200:
      print("ERROR2")

  # pp.pprint(resp.json())
  # pp.pprint(resp.json()['tracks'])
  # pp.pprint(resp.json()['tracks'][0])
  # print(len(resp.json()['tracks']))


  uri = resp.json()['tracks'][0]['uri']
  # print(resp.json()['tracks'][0]['name'], resp.json()['tracks'][0]['artists'][0]['name'])





  # ADD NEW TRACK TO PLAYLIST


  sp_auth = SpotifyOAuth(client_id="eae14429b373461aadc72104110154f9",
                                                client_secret="ada7bc6d1a1d4eada84cf382ae26c4f0",
                                                redirect_uri=redirect_uri,
                                                scope=scope,
                                                cache_path='.shjangcache')
  sp = spotipy.Spotify(auth_manager=sp_auth)


  gym_playlist_id = '5sHebLj2M8wPPc1rfLKtX9'
  # "https://open.spotify.com/embed/playlist/5sHebLj2M8wPPc1rfLKtX9?si=ulRKMYT9R8C7Scmcny3fJQ"


  sp.playlist_add_items(gym_playlist_id, [uri])


  return custom_response({"result": "good"}, 200)





@user_api.route('/add_playlist/cafe/<string:username>', methods=['GET'])
def add_cafe_playlist(username):
  user = UserModel.get_user_by_name(username)

  artist_id = user.artist_id
  genres = user.genres




  scope = "user-read-recently-played playlist-modify-public user-library-modify playlist-read-collaborative playlist-modify-private"
  redirect_uri = "https://www.roomy-pennapps.space/home/"
  # redirect_uri = "http://localhost:8080/"
  # redirect_uri = "https://papps2020.uc.r.appspot.com/user/callback/"
  # redirect_uri = "http://example.com/callback/"

  # username = 'shjang956'
  # token = util.prompt_for_user_token(username, scope, client_id ="eae14429b373461aadc72104110154f9", client_secret = "ada7bc6d1a1d4eada84cf382ae26c4f0", redirect_uri='https://www.roomy-pennapps.space/home/')
  token = True
  if token:

    sp_auth = SpotifyOAuth(client_id="eae14429b373461aadc72104110154f9",
                                                  client_secret="ada7bc6d1a1d4eada84cf382ae26c4f0",
                                                  redirect_uri=redirect_uri,
                                                  scope=scope)                                          
    sp = spotipy.Spotify(auth_manager=sp_auth)

    # sp = spotipy.Spotify(auth=token)


    # url = sp_auth.get_authorize_url()
    # print(url)

  else:
    # print("Can't get token for ", username)
    print("Error getting token")



  # artist_id, genres

  # Get random new songs from seeds (genre and artist)

  resp = requests.get('https://api.spotify.com/v1/recommendations/?market={}&seed_artists={}&seed_genres={}&min_energy={}&min_popularity={}'.format(
      'US', artist_id, ','.join(genres[:5]), 0.4, 50
  ),  headers = {'Authorization': '{} {}'.format(sp.auth_manager.get_cached_token()['token_type'], sp.auth_manager.get_cached_token()['access_token'])})
  if resp.status_code != 200:
      print("ERROR2")

  # pp.pprint(resp.json())
  # pp.pprint(resp.json()['tracks'])
  # pp.pprint(resp.json()['tracks'][0])
  # print(len(resp.json()['tracks']))


  uri = resp.json()['tracks'][0]['uri']
  # print(resp.json()['tracks'][0]['name'], resp.json()['tracks'][0]['artists'][0]['name'])





  # ADD NEW TRACK TO PLAYLIST


  sp_auth = SpotifyOAuth(client_id="eae14429b373461aadc72104110154f9",
                                                client_secret="ada7bc6d1a1d4eada84cf382ae26c4f0",
                                                redirect_uri=redirect_uri,
                                                scope=scope,
                                                cache_path='.shjangcache')
  sp = spotipy.Spotify(auth_manager=sp_auth)


  cafe_playlist_id = '2P8cx6O6JIu0sT2ItymYNI'
  # "https://open.spotify.com/embed/playlist/5sHebLj2M8wPPc1rfLKtX9?si=ulRKMYT9R8C7Scmcny3fJQ"


  sp.playlist_add_items(cafe_playlist_id, [uri])


  return custom_response({"result": "good"}, 200)










# @user_api.route('/get_spotify_info/callback/', methods=['GET'])
# def callback_route():
#   return custom_response({"result": "nice"}, 200)




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
