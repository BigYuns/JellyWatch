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
import webapp2
import users
import json
from google.appengine.ext import ndb

def send_json(handler, response):
    handler.response.headers['Content-Type'] = 'application/json'
    handler.response.headers['Access-Control-Allow-Origin'] = '*'
    handler.response.write(json.dumps(response))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("hey")

class TestPageHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(open('testpage.html').read())

class CreateOrUpdateAccountHandler(webapp2.RequestHandler):
    def post(self):
        token = self.request.get('token')
        if users.is_admin(token):
            email = self.request.get('email')
            password = self.request.get('password') # 'true' or 'false'
            is_admin = self.request.get('is_admin') # 'true' or 'false'
            is_organization = self.request.get('is_organization')
            
            user = users.User.with_email(email)
            if user:
                # update existing:
                if password: user.pwd_hash = users.hash_pwd(password)
                if is_admin is not None: user.is_admin = is_admin == 'true'
                if is_organization is not None: user.is_organization = is_organization == 'true'
                message = 'Updated user'
                user.put()
            else:
                # create new:
                if password is None or password == '' or email is None or email == '':
                    message = "Can't have an empty password or email"
                else:
                    user, message = users.User.create_user(email, password, is_organization == 'true', is_admin == 'true')
                    user.put()
            
            response = {"success": (user is not None), "message": message}
        else:
            response = {"success": False, "message": "Only admins can create new users"}
        
        send_json(self, response)

class DeleteUserHandler(webapp2.RequestHandler):
    def post(self):
        token = self.request.get('token')
        response = {}
        if users.is_admin(token):
            email = self.request.get('email')
            user = users.User.with_email(email)
            if user:
                user.key.delete()
                response = {"success": True}
            else:
                response = {"success": False, "message": "No user with this email found"}
        else:
            response = {"success": False, "message": "Only adins can delete users"}
        
        send_json(self, response)

class LoginHandler(webapp2.RequestHandler):
    def post(self):
        email = self.request.get('email')
        password = self.request.get('password')
        token = users.User.create_login_token(email, password)
        
        response = {"success": False, "token": None, "message": None}
        
        if token:
            user = users.user_for_token(token)
            response['token'] = token
            response['user'] = user.to_json()
            response['success'] = True
        else:
            response["message"] = "No matching user found"
        
        send_json(self, response)

class ListUsersHandler(webapp2.RequestHandler):
    def get(self):
        token = self.request.get('token')
        response = {}
        if users.is_admin(token):
            response = {"users": [u.to_json() for u in users.User.query()]}
        else:
            response = {"message": "Only admins can see the list of users"}
        
        send_json(self, response)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/test', TestPageHandler),
    ('/users', ListUsersHandler),
    ('/users/update', CreateOrUpdateAccountHandler),
    ('/users/delete', DeleteUserHandler),
    ('/users/login', LoginHandler)
], debug=True)
