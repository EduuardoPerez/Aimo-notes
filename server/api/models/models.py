# Python
import os
# Peewee
from peewee import (
    SqliteDatabase,
    Model,
    AutoField,
    CharField,
    TextField,
    ForeignKeyField,
)


db = SqliteDatabase(os.getenv('DATABASE_PATH'))


class BaseModel(Model):
    """Base model class. All children share the same database"""
    id = AutoField()

    class Meta:
        database = db


class User(BaseModel):
    """Note model class"""
    email = CharField(max_length=80, unique=True)
    password = CharField()

class Note(BaseModel):
    """Note model class"""
    title = CharField()
    content = TextField()
    user = ForeignKeyField(User)
