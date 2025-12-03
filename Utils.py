import hashlib
import random
import numpy as np

def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password


def check_password(hashed_password,plain_password):
    if hashed_password == hash_password(plain_password):
        return True
    else:
        return False


def generate_card_number():
    digits = np.random.randint(0,10,16)
    card_number = ''.join(digits.astype(str))
    return card_number