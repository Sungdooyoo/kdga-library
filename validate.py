import re


USER_RE = re.compile(r"^.{2,5}$")
PWD_RE = re.compile(r"^.{6,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
PHONE_RE = re.compile(r"^[0-9]{11}$")
def valid_username(username):
    if username:
      return USER_RE.match(username)
    else:
      return None

def valid_password(password):
    if password:
      return PWD_RE.match(password)
    else:
      return None

def valid_email(email):
    if email:
      return EMAIL_RE.match(email)
    else:
      return None

def valid_phoneNumber(phoneNumber):
    if phoneNumber:
      return PHONE_RE.match(phoneNumber)
    else:
      return None
