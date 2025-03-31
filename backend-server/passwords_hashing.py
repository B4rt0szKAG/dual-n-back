import bcrypt
import re

def hash_pass(user_password: str) -> bytes:
    bytes = user_password.encode()

    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(bytes, salt)

    return hashed_pass

def check_pass(user_password: str , hash: bytes) -> bool:
    bytes = user_password.encode()

    return bcrypt.checkpw(bytes, hash)

def check_pass_strength(user_password) -> tuple[bool, str]:

    if len(user_password) < 8:
        return (False, "Password is too short, at least 8 signs are required ")
    if not re.search(r"[A-Z]",user_password):
        return (False,"Password needs to contain, at least one Big letter")
    if not re.search(r"\d", user_password):
        return (False,"Password needs to contain, at least one number")
    if not re.search(r"[!@#$%^&*]"):
        return (False, "Password needs to contain, at least one Special sign")
    else:
        return (True, "Password correct")



