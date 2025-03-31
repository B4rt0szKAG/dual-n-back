import sqlite3

def duplicate_check(username: str) -> bool:
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("select username from users where username = ?",(username,))
    result = cursor.fetchone()
    conn.close()

    if result == None:
        return True
    return False

def username_length(username:str) -> bool:
    if len(username) > 3: return True
    return False
