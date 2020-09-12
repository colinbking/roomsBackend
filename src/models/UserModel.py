# src/models/UserModel.py
from marshmallow import fields, Schema
from sqlalchemy.sql import operators
from sqlalchemy.dialects.postgresql import ARRAY
import datetime
from . import db, bcrypt

class UserModel(db.Model):
  """
  User Model
  """

  # table name
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(128), nullable=False)
  user_id = db.Column(db.String(128), nullable=False)
  email = db.Column(db.String(128), unique=True, nullable=False)
  artist = db.Column(db.String(128), nullable=False)
  genres = db.Column(ARRAY(db.String(128)), nullable=False)
  songs = db.Column(ARRAY(db.String(128)), nullable=False)
  zoom_token = db.Column(db.String(256))
  created_at = db.Column(db.DateTime)
  status = db.Column(db.String(128))
  online = db.Column(db.Boolean(128))
  last_seen_in = db.Column(db.String(128))
  last_login = db.Column(db.DateTime)

  # class constructor
  def __init__(self, id, username, email):
    """
    Class constructor
    """
    self.username = username
    self.email = email
    self.id = id
    self.user_id = email
    self.created_at = datetime.datetime.utcnow()
    self.modified_at = datetime.datetime.utcnow()
    self.online = True

  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    for key, item in data.items():
      if key == 'password':
        self.password = self.__generate_hash(value)
      setattr(self, key, item)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  @staticmethod
  def get_all_users():
    return UserModel.query.all()

  @staticmethod
  def get_one_user(id):
    return UserModel.query.get(id)
  
  @staticmethod
  def get_user_by_name(value):
    return UserModel.query.filter_by(username=value).first()

  @staticmethod
  def get_user_by_email(value):
    return UserModel.query.filter_by(email=value).first()

  def __generate_hash(self, password):
    return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
  
  def check_hash(self, password):
    return bcrypt.check_password_hash(self.password, password)
  
  def __repr(self):
    return '<id {}>'.format(self.id)

class UserSchema(Schema):
  id = fields.Int()
  user_id = fields.Str()
  username = fields.Str(required=True)
  email = fields.Email(required=True)
  artist = fields.Str()
  genres = fields.List(fields.Str)
  songs = fields.List(fields.Str)
  zoom_token = fields.Str()
  status = fields.Str()
  last_seen_in = fields.Str()
  last_login = fields.Str()
  online = fields.Bool()
  created_at = fields.DateTime(default=datetime.datetime.utcnow())

#   blogposts = fields.Nested(BlogpostSchema, many=True)

