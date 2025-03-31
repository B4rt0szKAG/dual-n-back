import sqlite3
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.executescript("""
    CREATE TABLE IF NOT EXISTS Statistics (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Users_ID integer NOT NULL,
    Day date NOT NULL,
    type_of_game text NOT NULL,
    points_scored integer NOT NULL,
    CONSTRAINT Statistics_Users FOREIGN KEY (Users_ID)
    REFERENCES Users (ID)
);

-- Table: Users
CREATE TABLE IF NOT EXISTS Users (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    username varchar(50) NOT NULL,
    name varchar(50) NOT NULL,
    lastname varchar(50) NOT NULL,
    email varchar(50) NOT NULL,
    password varchar(50) NOT NULL
);

""")

cursor.execute("INSERT INTO Users (username, name, lastname, email, password) VALUES (?,?,?,?,?)",("pawciogaa","pawel","gala","aaa@gmail.com","abcd1234"))
conn.commit()

cursor.execute("select * from Users")
print(cursor.fetchall())

def add_user(user):
    cursor.execute("INSERT INTO Users (username, name, lastname, email, password) "
                   "VALUES (?,?,?,?,?)",(user.username,user.name,user.lastname,user.email,user.password))
    conn.commit()
    conn.close()

def del_user_and_his_stats(user_id):

    cursor.execute(f"DELETE * from Statistics where Users_ID = {user_id}")

    cursor.execute(f"DELETE from Users where ID = {user_id}")

    conn.commit()
    conn.close()

def del_stats(user_id,from_day,to_day):
    cursor.execute(f"DElETE from Statistics where Users_ID = {user_id} and Day between {from_day} and {to_day} ")

    conn.commit()
    conn.close()

def add_stats(stats):
    cursor.execute("INSERT INTO Statistics (Users_ID,Day,type_of_game,points_scored) Values (?,?,?,?,?)",
                   (stats.user_ID,stats.day, stats.type_of_game, stats.points_scored))

    conn.commit()
    conn.close()

    #TODO do każdego zapytania dodać token potwierdzający użytkownika, token będzie wysyłąny przez serwer do użytkownika podczas logowania