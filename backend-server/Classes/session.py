from .baseModel import BaseModel
from peewee import IntegerField, CharField, DateField
from peewee import *
from .user import User
import datetime


class SessionToken(BaseModel):
    token = CharField(primary_key=True)
    user = ForeignKeyField(User, backref='sessions')
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    expires_at = DateTimeField()