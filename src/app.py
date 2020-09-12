#src/app.py

from flask import Flask

from .config import app_config
from .models import db, bcrypt

# import user_api blueprint
from .views.UserView import user_api as user_blueprint
from .views.BigRoomView import br_api as br_blueprint
from .views.GymView import gym_api as gym_blueprint



def create_app(env_name):
  """
  Create app
  """
  
  # app initiliazation
  app = Flask(__name__)

  app.config.from_object(app_config[env_name])

  # initializing bcrypt and db
  bcrypt.init_app(app)
  db.init_app(app)
#   app.config["SSE_REDIS_URL"] = 

  app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')
  app.register_blueprint(br_blueprint, url_prefix='/api/v1/br')
  app.register_blueprint(gym_blueprint, url_prefix='/api/v1/gym')



  @app.route('/', methods=['GET'])
  def index():
    """
    example endpoint
    """
    return 'ROOMS'

  return app

