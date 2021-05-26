# Peewee
from peewee import Model, AutoField
# api
from api.app import db

class BaseModel(Model):
    """Base model class. All children share the same database"""
    id = AutoField()

    class Meta:
        database = db


