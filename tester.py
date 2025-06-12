from backend_server.client import *
from datetime import date

user = User(
    username="pelikan3",
    name="Maciek",
    lastname="Kowalski",
    email="maciek@example.com",
    password="ECT9Cllzu47gQOk!!"
)
#

# register(user)

stats = Statistics(
    user_name = 'pelikan3',
    day = date.today(),
    points_scored=15
)
logIn(user.username, user.password)
# saveLocalStats(stats,"pelikan")


# print(newstats)
#

# time.sleep(10)
# try:
#     sendStats(stats,'pelikan3')
# except SendingDataError:
#     print('nie dziala')



# time.sleep(30)

# try:
#     logOut(user.username)
# except NoAuthFile:
#     print('nie ma pliku auth')
#
# except ErrorlogOut:
#     print("wywlailo się wylogowanie")

# getStats("LAST_30_DAYS")
