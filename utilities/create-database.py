import os
import projectpath
from peewee import SqliteDatabase
from dotenv import load_dotenv
from api.models import User, Note, db

load_dotenv('../.env')

db.init(os.getenv('DATABASE_PATH'))
db.connect()
db.create_tables([
    User,
    Note
])

# This was the test from the server.api.models
# def create_tables():
#     db.init(os.getenv('DATABASE_PATH'))
#     db.connect()
#     User.create_table(True)
#     Note.create_table(True)