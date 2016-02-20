#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import hashlib
import hmac
import webapp2
import cgi
import jinja2
from google.appengine.ext import db

import s_hash
import cookie
import validate 


template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), 
                                                                autoescape=True)

# Entities for Datastore 
class User(db.Model):
    user_id = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    email = db.EmailProperty(required = True)
    created_time = db.DateTimeProperty(auto_now_add = True)


# Webpage Handlers that handles http request and responses to render pages
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Main(Handler):
    def get(self):
        self.write("hi")

    def post(self):
        pass



class Signup(Handler):
    def get(self):
        # self.response.set_cookie("login_success","true")
        self.render("signup.html")

    def post(self):
        username = self.request.get("username")
        user_email = self.request.get("email")
        user_phoneNumber = self.request.get("phoneNumber")
        password = self.request.get("password")
        password_check = self.request.get("confirm_password")        

        #validate user inputs
        valid_input = False
        if validate.valid_username(username) == False:
            self.error_caused_by("username")
        elif validate.valid_email(user_email) == False:
            self.error_caused_by("email")
        elif validate.valid_phoneNumber(user_phoneNumber) == False:
            self.error_caused_by("phoneNumber")           
        elif validate.valid_password(password) == False:
            self.error_caused_by("password")
        elif password != password_check:
            self.error_caused_by("confirm_password")
        elif self.check_existing_user(username):
            self.error_caused_by("Your user name is taken")

        #else:
            # self.response.set_cookie("login_success","true")
            # self.response.set_cookie("failed_reason","not failed")

            # password = s_hash.hash_password(password)
            # user_instance = User(user_id = username,email= user_email, password = password)
            # user_instance.put()            
            # self.response.set_cookie("logged_in_username", s_hash.hash_cookie(user_id))
            # self.redirect("/welcome")        


    def error_caused_by(self, failed_reason):
        self.response.set_cookie("login_success","false")
        self.response.set_cookie("failed_reason", failed_reason)
        self.redirect("/signup?error=%s" % failed_reason)



app = webapp2.WSGIApplication([('/', Main), 
                               ('/signup',Signup),
                               ], debug=True)
