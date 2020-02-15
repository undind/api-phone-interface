import os
from datetime import datetime
from config import db
from models import Contacts, History

CONTACTS_LIST = [
  {
    "first_name": "Sergey",
    "last_name": "Antonov",
    "phone_number": "79780070707",
    "date_birth": "2011-01-08",
    "histories": [
      ("2019-12-06 22:17:54"),
      ("2019-12-06 22:17:54"),
      ("2019-12-06 22:17:54"),
      ("2018-11-06 22:18:54")
    ]
  },
  {
    "first_name": "Victor",
    "last_name": "Ivanov",
    "phone_number": "79780010101",
    "date_birth": "2012-01-08",
    "histories": [
      ("2019-09-06 12:17:54"),
      ("2019-12-06 22:17:54"),
      ("2019-12-06 22:17:54")
    ]
  },
  {
    "first_name": "Egor",
    "last_name": "Petrov",
    "phone_number": "79710020301",
    "date_birth": "1999-01-08",
    "histories": [
      ("2019-01-05 22:17:54"),
      ("2019-11-06 22:17:54"),
      ("2019-12-06 12:17:54")
    ]
  },
  {
    "first_name": "Peter",
    "last_name": "Jacobson",
    "phone_number": "72780272317",
    "date_birth": "2011-01-18",
    "histories": [
      ("2019-01-08 22:17:54"),
      ("2019-11-06 12:17:54"),
    ]
  }
]


if os.path.exists('contacts.db'):
  os.remove('contacts.db')


db.create_all()


for contacts in CONTACTS_LIST:
  con = Contacts(first_name=contacts.get('first_name'), last_name=contacts.get('last_name'), phone_number=contacts.get('phone_number'), date_birth=contacts.get('date_birth'))

  for his in contacts.get('histories'):
    created_at = his
    con.histories.append(
      History(
        created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
      )
    )

  db.session.add(con)


db.session.commit()
