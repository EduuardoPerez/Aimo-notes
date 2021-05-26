# Peewee
from peewee import CharField, TextField, ForeignKeyField

from .base import BaseModel
from .users import User

class Note(BaseModel):
    """Note model class"""
    title = CharField()
    content = TextField()
    user = ForeignKeyField(User)
