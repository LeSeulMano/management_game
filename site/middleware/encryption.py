import hashlib
import random
from datetime import datetime

def hash_shab512(value: str):
    # h = hashlib.sha512()
    hash_object = hashlib.sha512(value.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig

def token(login):
    random_number:int = random.randint(10**15, 10**16-1)
    date = str(datetime.now())[:-7:]
    token = ''
    token += hash_shab512(str(random_number)) + hash_shab512(date) + hash_shab512(login)
    return hash_shab512(token)