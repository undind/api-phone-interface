from flask import abort, make_response
from config import db
from models import History, HistorySchema, Contacts


def get_all():
  stories = History.query.order_by(db.desc(History.created_at)).all()

  if stories is not None:
    stories_schema = HistorySchema(many=True)
    return stories_schema.dump(stories)
  
  else:
    abort(404, "Nothing found")


def get_once_history(contact_id, history_id):
  story = (
    History.query.join(Contacts, Contacts.contact_id == History.contact_id)
    .filter(Contacts.contact_id == contact_id)
    .filter(History.history_id == history_id)
    .one_or_none()
  )

  if story is not None:
    story_schema = HistorySchema()
    return story_schema.dump(story)

  else:
    abort(404, "History not found!")


def create_history(contact_id, history):
  contacts = Contacts.query.filter(Contacts.contact_id == contact_id).one_or_none()

  if contacts is None:
    abort(404, "Contact not found!")

  schema = HistorySchema()
  new_story = schema.load(history, session=db.session)

  contacts.histories.append(new_story)
  db.session.commit()

  data = schema.dump(new_story)

  return data, 201


def delete_story(contact_id, history_id):
  story = (
    History.query.filter(Contacts.contact_id == contact_id)
    .filter(History.history_id == history_id)
    .one_or_none()
  )

  if story is not None:
    db.session.delete(story)
    db.session.commit()
    
    return make_response(
      "History deleted", 200
    )

  else:
    abort(404, "History not found!")