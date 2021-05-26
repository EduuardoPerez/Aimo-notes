# Peewee
from peewee import CharField

from .base import BaseModel

class User(BaseModel):
    """Note model class"""
    email = CharField(max_length=80, unique=True)
    password = CharField()
