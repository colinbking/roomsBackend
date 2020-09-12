# src/models/UserModel.py
from marshmallow import fields, Schema
import datetime
from . import db, bcrypt
from sqlalchemy.sql import operators
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
  workoutlink = db.Column(db.String(128), nullable=False)
  activemembers = db.Column(ARRAY(db.String(128)), nullable=False)
  
  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.name = data.get('name')
    self.activemembers = data.get('activemembers')
    self.focus = data.get('focus')
    self.workoutlink = data.get('workoutlink')

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
  activemembers = fields.List(fields.Int)
  workoutlink = fields.Str()

#   blogposts = fields.Nested(BlogpostSchema, many=True)

