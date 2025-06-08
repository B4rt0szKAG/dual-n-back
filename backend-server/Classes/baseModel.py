from peewee import *
import datetime

db = SqliteDatabase('database.db')

class BaseModel(Model):
    class Meta:
        database = db

