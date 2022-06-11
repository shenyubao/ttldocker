import string
import random


def strong_password():
    password = random.sample(string.ascii_lowercase, 6) + random.sample(string.ascii_uppercase, 6) + random.sample(string.digits, 6)
    random.shuffle(password)
    return "".join(password)
