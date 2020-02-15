from datetime import datetime
from config import db, ma
from marshmallow import fields
from sqlalchemy import ForeignKeyConstraint


class MyDateTime(db.TypeDecorator):
  impl = db.DateTime
    
  def process_bind_param(self, value, dialect):
    if type(value) is str:
        return datetime.strptime(value, '%Y-%m-%d')
    return value

class Contacts(db.Model):
  __tablename__ = "contacts"
  contact_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  first_name = db.Column(db.String(32), nullable=False)
  last_name = db.Column(db.String(32), nullable=False)
  date_birth = db.Column(MyDateTime, default=datetime.now)
  phone_number = db.Column(db.Integer, nullable=False)
  created_at = db.Column(
    db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
  )
  histories = db.relationship(
    "History",
    backref="contacts",
    cascade="all, delete, delete-orphan",
    single_parent=True,
    order_by="desc(History.created_at)"
  )


class History(db.Model):
  __tablename__ = "history"
  history_id = db.Column(db.Integer, primary_key=True)
  contact_id = db.Column(db.Integer, db.ForeignKey("contacts.contact_id"))
  created_at = db.Column(
    db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
  )
  db.ForeignKeyConstraint(
    ["contact_id"],
    ["contacts.contact_id"]
  )


class ContactsSchema(ma.ModelSchema):
  class Meta:
    model = Contacts
    sqla_session = db.session

  histories = fields.Nested("ContactsHistorySchema", default=[], many=True)


class ContactsHistorySchema(ma.ModelSchema):
  history_id = fields.Int()
  created_at = fields.Str()


class HistorySchema(ma.ModelSchema):
  class Meta:
    model = History
    sqla_session = db.session

  contacts = fields.Nested("HistoryContactSchema", default=None)


class HistoryContactSchema(ma.ModelSchema):
  contact_id = fields.Int()
  first_name = fields.Str()
  last_name = fields.Str()
  phone_number = fields.Int()
