from .baseModel import BaseModel
from peewee import CharField


class User(BaseModel):
    username = CharField(unique=True)
    name = CharField()
    lastname = CharField()
    email = CharField()
    password = CharField()
