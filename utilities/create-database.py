import os
import projectpath
from peewee import SqliteDatabase
from dotenv import load_dotenv
from api.models import User, Note
from api.app import db

load_dotenv('../.env')

db.init(os.getenv('DATABASE_PATH'))
db.connect()
db.create_tables([
    User,
    Note
])
