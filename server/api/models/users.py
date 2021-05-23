import os
from peewee import SqliteDatabase, CharField, Model

db = SqliteDatabase(os.getenv('DATABASE_PATH'))

class User(Model):
    name = CharField()
    email = CharField(unique=True)
    token = CharField()

    class Meta:
        database = db
