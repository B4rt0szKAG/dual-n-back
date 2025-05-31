from Classes.user import User
from Classes.session import SessionToken
from Classes.statstics import Statistics
# # users = User.select()
tokens = SessionToken.select()
stats = Statistics.select()
# for user in users:
#     print(user.username, user.email)
#
for token in tokens:
    print(token.token,token.user_name.username)

for stat in stats:
    print(stat.user_name,stat.day,stat.type_of_game,stat.points_scored)

# User.drop_table()
# SessionToken.drop_table()
# Statistics.drop_table()