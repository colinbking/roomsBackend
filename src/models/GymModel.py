# src/models/UserModel.py
from marshmallow import fields, Schema
import datetime
from . import db, bcrypt
from sqlalchemy.sql import operators
from sqlalchemy import DateTime
# from sqlalchemy import ARRAY
from sqlalchemy.dialects.postgresql import ARRAY

class GymModel(db.Model):
  """
  gym Room Model
  """

  # table name
  __tablename__ = 'gym'

  id = db.Column(db.Integer, primary_key=True)
  lastplayed = db.Column(db.String(128), nullable=False)
  focus = db.Column(db.String(128), nullable=False)
  video = db.Column(db.String(128), nullable=False)
  video_started = db.Column(DateTime, default=None)
  active = db.Column(ARRAY(db.String(128)), nullable=False)
  
  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.lastplayed = data.get('lastplayed')
    self.active = data.get('active')
    self.focus = data.get('focus')
    self.video = data.get('video')
    self.video_started = data.get('video_started')


  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    for key, item in data.items():
      setattr(self, key, item)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  @staticmethod
  def get_all_gyms():
    return GymModel.query.all()

  @staticmethod
  def get_one_gym(id):
    return GymModel.query.get(id)

  @staticmethod
  def join_gym(id):
    return GymModel.query.get(id)


  def __repr(self):
    return '<id {}>'.format(self.id)

class GymSchema(Schema):
  id = fields.Int(dump_only=True)
  lastplayed = fields.Str()
  focus = fields.Str()
  active = fields.List(fields.Str)
  video = fields.Str()
  video_started = fields.DateTime()


#   blogposts = fields.Nested(BlogpostSchema, many=True)

