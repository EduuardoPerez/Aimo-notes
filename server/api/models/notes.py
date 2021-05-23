import os
from peewee import SqliteDatabase, CharField, ForeignKeyField, Model
from bottle import hook
from .users import User

db = SqliteDatabase(os.getenv('DATABASE_PATH'))

class Note(Model):
    title = CharField()
    content = CharField()
    owner = ForeignKeyField(User)


    class Meta:
        database = db
