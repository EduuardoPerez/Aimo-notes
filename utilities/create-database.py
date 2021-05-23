import os
import projectpath
from peewee import SqliteDatabase
from dotenv import load_dotenv
from api.models import User, Note

load_dotenv('../.env')

db = SqliteDatabase(os.getenv('DATABASE'))
User._meta.database = db
Note._meta.database = db

db.connect()
db.create_tables([User, Note])