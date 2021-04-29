import random
import string
from .db import *
import jwt
import datetime
from config import FLASK_SECRET

def generate_id():
    _id = random.randint(10000000000,99999999999)
    if not is_used("users", idc=_id):
        return _id
    else:
        generate_id()

def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=100))

def generate_jwt():
    return str(jwt.encode({"expire":int((datetime.datetime.now() + datetime.timedelta(days=2)).timestamp())}, FLASK_SECRET, algorithm='HS256'))