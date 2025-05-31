from .baseModel import BaseModel
from peewee import CharField


class User(BaseModel):
    username = CharField(primary_key=True)
    name = CharField()
    lastname = CharField()
    email = CharField()
    password = CharField()
