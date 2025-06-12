from .baseModel import BaseModel
from peewee import IntegerField, CharField, DateField
from peewee import *
from .user import User
import datetime

class Statistics(BaseModel):
    user_name = ForeignKeyField(User, backref='stats')
    day = DateField()
    points_scored = IntegerField()


    def to_dict(self):
        username = self.user_name.username if isinstance(self.user_name, User) else self.user_name
        return {
            'user_name': username,
            'day': self.day.isoformat(),  # datetime na string
            'points_scored': self.points_scored
        }