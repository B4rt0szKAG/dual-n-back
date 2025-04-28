from Classes.user import User

users = User.select()

for user in users:
    print(user.username, user.email)