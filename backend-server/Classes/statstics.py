from .baseModel import BaseModel
from peewee import IntegerField, CharField, DateField


class Statistics(BaseModel):
    user_ID = IntegerField()
    day = DateField()
    type_of_game = CharField()
    points_scored = IntegerField()
