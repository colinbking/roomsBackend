# BACKEND REPOSITORY FOR http://roomy-pennapps.space/
Part of a top 10 project for PennApps XXI: https://devpost.com/software/roomy

# Roomy Backend API
backend deployment: https://papps2020.uc.r.appspot.com/ 

## Installation
  - Install [Python](https://www.python.org/downloads/), [Pipenv](https://docs.pipenv.org/) and [Postgres](https://www.postgresql.org/) on your machine
  - Clone the repository `$ git clone https://github.com/olawalejarvis/blog_api.git`
  - Change into the directory `$ cd /blog_api`
  - Activate the project virtual environment with `$ pipenv shell` command
  - Install all required dependencies with `$ pipenv install`
  - Export the required environment variables
  - Start the app with `python main.py`


<h3>USERS</h3>
(GET) /user/:  
returns all users


(GET) /user/<string:username>/get_spotify_info:
  updates the user specified to have updated genres and artists from their most recently played; prompts spotify login.


(POST) /user/<string:username>/zoom_login:
- needs the auth_code from the redirect url in a json parameter as a value for the key "auth_code".
- returns the full user information, with the zoom token, for the provided user id

<h3>BIG ROOM</h3>
(GALLERY VIEW OF ROOMS)  
(GET) /br/<int:br_id>:
returns the data for a specific bigroom object with id based on uri param, in the following format: 
{  
 id = fields.Int(dump_only=True)  
  name = fields.Str()  
  members = fields.List(fields.Int)  
  active = fields.List(fields.Str)  
  gym_id = fields.Int()  
  cafe_id = fields.Int()  
  kitchen_id = fields.Int()  
}  

(GET) /br/<int:br_id>/whos_active:
 returns list of active usernames

(PUT) /br/<int:br_id>/joined_br:
-requires "username" and "id" fields in json payload.
makes the user specified in the payload join the big room
returns updated list of active usernames in the big room


(PUT) /br/<int:br_id>/left_br:
-requires "username" and "id" fields in json payload.
makes hte user specified in payload leave the big room
returns updated list of active usernames in the big room


<h3>GYM</h3>
  
(GET) /gym/<int:gym_id>:  
 returns json data for one gym room
 
(GET) /gym/<int:gym_id>/whos_active:  
 returns list of active usernames in gym  

(PUT) /br/<int:gym_id>/joined_gym:  
-requires "username" and "id" fields in json payload.  
makes the user specified in the payload join the gym.  
if the first person, starts a zoom meeting, and returns zoom meeting link under "meeting" key in response json.  
returns updated list of active usernames in the big room under "active_members" key in response json.  

(PUT) /br/<int:gym_id>/left_gym:   
-requires "username" and "id" fields in json payload.  
makes the user specified in the payload leave the gym.   
returns updated list of active usernames in the big room   

(PUT) /br/<int:gym_id>/start_workout:  
-sets the current timestamp as the time the workout was started.    
-send a GET to workout start to retrieve this (when a late person joins, will do this)   
-returns timestamp in utc of when workout was staretd  

(GET) /br/<int:gym_id>/join_workout:  
returns integer difference of number of seconds you should skip ahead in the video to catch up

(PUT) /br/<int:gym_id>/set_note:  
takes value of "note" key in payload and sets it as the "note" field of the room (status thing to query from big room view)












