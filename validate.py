import re


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PWD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_username(username):
    if username:
      return USER_RE.match(username)
    else:
      return False

def valid_password(password):
    if password:
      return PWD_RE.match(password)
    else:
      return False

def valid_email(email):
    if email:
      return EMAIL_RE.match(email)
    else:
      return False

