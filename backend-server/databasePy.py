from Classes.statstics import Statistics
from Classes.user import User
from Classes.baseModel import db
from Classes.session import SessionToken


db.connect()

db.create_tables([User,Statistics,SessionToken])

db.close()