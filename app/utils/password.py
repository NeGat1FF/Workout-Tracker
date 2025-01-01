from argon2 import PasswordHasher

ph = PasswordHasher()

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(hashed_password: str, password: str):
    try:
        return ph.verify(hashed_password, password)
    except:
        return False
