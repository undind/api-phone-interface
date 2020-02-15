from flask import abort, make_response
from config import db
from models import Contacts, ContactsSchema, History


def get_contacts():
  contacts = Contacts.query.order_by(Contacts.first_name).all()

  if contacts is not None:
    contacts_schema = ContactsSchema(many=True, only=['contact_id', 'first_name', 'last_name', 'date_birth', 'phone_number'])
    return contacts_schema.dump(contacts)
  
  else:
    abort(404, "Nothing found")

  
def get_once_contact(contact_id):
  contact = Contacts.query.filter(Contacts.contact_id == contact_id).outerjoin(History).one_or_none()

  if contact is not None:
    contact_schema = ContactsSchema(only=['contact_id', 'first_name', 'last_name', 'date_birth', 'phone_number', 'histories'])

    return contact_schema.dump(contact)

  else:
    abort(404, "Contact not found")


def create_contact(contact):
  fname = contact.get('first_name')
  lname = contact.get('last_name')
  phnumber = contact.get('phone_number')
  birth = contact.get('date_birth')

  exist_contact = Contacts.query.filter(Contacts.first_name == fname).filter(Contacts.last_name == lname).filter(Contacts.phone_number == phnumber).one_or_none()

  if exist_contact is None:
    schema = ContactsSchema()
    new_contact = schema.load(contact, session=db.session)

    db.session.add(new_contact)
    db.session.commit()

    data = schema.dump(new_contact)
    return data, 201

  else:
    abort(409, "Contact {fname} {lname} allready exists".format(fname=fname, lname=lname))


def update_contact(contact_id, contact):
  update_contact = Contacts.query.filter(Contacts.contact_id == contact_id).one_or_none()

  if update_contact is not None:
    schema = ContactsSchema()
    update = schema.load(contact, session=db.session)

    update.contact_id = update_contact.contact_id

    db.session.merge(update)
    db.session.commit()

    data = schema.dump(update_contact)
    return data, 200

  else:
    abort(404, "Contact not found")


def delete_contact(contact_id):
  contact = Contacts.query.filter(Contacts.contact_id == contact_id).one_or_none()

  if contact is not None:
    db.session.delete(contact)
    db.session.commit()
    return make_response("Contact deleted", 200)

  else:
    abort(404, "Contact not found")
