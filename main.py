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
        self.render("signup.html")

    def post(self):
        #get user_input and store in variables
        pass





app = webapp2.WSGIApplication([('/', Main), 
                               ('/signup',Signup),
                               ], debug=True)
