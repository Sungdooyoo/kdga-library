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

# -*- coding: utf-8 -*-
import os
import hashlib
import hmac
import webapp2
import cgi
import jinja2
import urllib
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
    phoneNumber = db.IntegerProperty(required = True)
    created_time = db.DateTimeProperty(auto_now_add = True)


# Webpage Handlers that handles http request and responses to render pages
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.headers['Content-Type'] = "text/html;charset=utf-8"
        self.response.charset = "utf-8"
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Main(Handler):
    def get(self):
        username = self.request.cookies.get("username")
        self.render("index.html", username=username)
    def post(self):
        pass



class Signup(Handler):
    def get(self):
        # self.response.set_cookie("login_success","true")
        self.render("signup.html")

    def post(self):
        username = self.request.get("username")
        user_phoneNumber = self.request.get("phoneNumber")
        password = self.request.get("password")
        password_check = self.request.get("confirm_password")        

        #validate user inputs
        valid_input = False
        if validate.valid_username(username) == None:
            self.error_caused_by("username",username=username, phoneNumber=user_phoneNumber)
        elif validate.valid_phoneNumber(user_phoneNumber) ==  None:
            self.error_caused_by("phoneNumber" , username=username, phoneNumber=user_phoneNumber)           
        elif validate.valid_password(password) == None:
            self.error_caused_by("password", username=username, phoneNumber=user_phoneNumber)
        elif password != password_check:
            self.error_caused_by("confirm_password",username=username, phoneNumber=user_phoneNumber)
        elif self.check_existing_user(username):
            self.error_caused_by("same_id",phoneNumber=user_phoneNumber)

        else:
            self.response.set_cookie("login_success","true")
            self.response.set_cookie("failed_reason","not failed")

            password = s_hash.hash_password(password)
            user_phoneNumber = int(user_phoneNumber)
            user_instance = User(user_id = username,phoneNumber=user_phoneNumber, password = password)
            user_instance.put()            
            self.response.set_cookie("username", username)
            self.render("index.html", username=username)


    def error_caused_by(self, failed_reason, username='', phoneNumber='',password=''):
        self.response.set_cookie("login_success","false")
        self.response.set_cookie("failed_reason", failed_reason)
        self.response.set_cookie("username", username)
        self.response.set_cookie("phoneNumber", phoneNumber)
        self.redirect("/signup?error=%s" % failed_reason)

    def check_existing_user(self, user_id):
        user_already_exists = False
        user_entries = db.GqlQuery("select * from User where user_id='%s'" % user_id )
        for user_entry in user_entries:
            if user_entry.user_id == user_id:
                user_already_exists = True 

        return user_already_exists        

class Signin(Handler):
    def get(self):
        self.render("signin.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        user_entries = db.GqlQuery("select * from User where user_id='%s'" % username )

        if user_entries.get():
            for entry in user_entries:
                if entry.user_id != "":
                    hash_val= entry.password.split('|')[0]
                    salt = entry.password.split('|')[1]
                    if hashlib.sha256(password + salt).hexdigest() == hash_val:
                        #login Success
                        # self.response.set_cookie("logged_in_username", s_hash.hash_cookie(username))
                        self.response.set_cookie("username",username)
                        self.redirect("/")
                    else:
                        self.response.set_cookie("failed_reason", "Invalid Password")
                        self.response.set_cookie("login_success", "false")
                        self.render("/signin")
        else:
            self.response.set_cookie("login_success", "false")
            self.response.set_cookie("failed_reason", "No such User")
            self.render("signin.html")


app = webapp2.WSGIApplication([('/', Main), 
                               ('/signup',Signup),
                               ('/signin',Signin),
                               ], debug=True)
