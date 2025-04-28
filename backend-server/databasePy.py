from Classes.statstics import Statistics
from Classes.user import User
from Classes.baseModel import db


db.connect()

db.create_tables([User,Statistics])

db.close()