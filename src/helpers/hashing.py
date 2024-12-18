import bcrypt


def hash_password(password: str):
    hashed_password = bcrypt.hashpw(
        password.encode(), bcrypt.gensalt(rounds=12)
    ).decode()
    return hashed_password


def compare_password(plain_password: str, hashed_password: str):
    password = bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
    if password:
        return True
    return False
