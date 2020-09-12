# src/models/UserModel.py
from marshmallow import fields, Schema
import datetime
from . import db, bcrypt
from sqlalchemy.sql import operators
# from sqlalchemy import ARRAY
from sqlalchemy.dialects.postgresql import ARRAY

class BigRoomModel(db.Model):
  """
  Big Room Model
  """

  # table name
  __tablename__ = 'bigroom'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  members = db.Column(ARRAY(db.String(128)), nullable=False)
  gymid = db.Column(db.Integer)
  

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.name = data.get('name')
    self.members = data.get('members')
    self.gymid = data.get('gymid')

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
  def get_all_big_rooms():
    return BigRoomModel.query.all()

  @staticmethod
  def get_one_big_room(id):
    return BigRoomModel.query.get(id)

  @staticmethod
  def join_bigroom(id):
    return BigRoomModel.query.get(id)


  def __repr(self):
    return '<id {}>'.format(self.id)

class BigRoomSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True)
  members = fields.List(fields.Int)
  gymid = fields.Int()

#   blogposts = fields.Nested(BlogpostSchema, many=True)

