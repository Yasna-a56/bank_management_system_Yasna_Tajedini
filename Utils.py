import hashlib

def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password


def check_password(hashed_password,plain_password):
    if hashed_password == hash_password(plain_password):
        return True
    else:

        return False
