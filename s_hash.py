import hmac
import random
import string
import hashlib

def validate_cookie(cookie):
    if cookie.find('|')>-1:
        cookie_val = cookie.split('|')[0]
        cookie_hash_val = cookie.split('|')[1]
        return hmac.new("secret",cookie_val).hexdigest() == cookie_hash_val
    else:
        return False

def hash_cookie(cookie):
    cookie = str(cookie)
    cookie_hash = hmac.new("secret", cookie).hexdigest()
    return cookie + "|" + cookie_hash

def hash_password(password):
    salt = make_salt()
    hashed_password = hashlib.sha256(password + salt).hexdigest()
    return hashed_password + "|" + salt

def make_salt():
    return "".join(random.choice(string.letters) for x in xrange(5))