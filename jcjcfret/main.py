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

from google.appengine.api import users
from google.appengine.ext import ndb

import models

class MainHandler(webapp2.RequestHandler):
    def get(self):

        #fetch current user and make a user profile key
        user = users.get_current_user()
        user_profile_key = ndb.Key("UserProfile", user.user_id())

        user_profile = user_profile_key.get()
        #user profile doesn't exist so we will create one
        if user_profile is None:
            user_profile = models.UserProfile(
                key = user_profile_key,
                user = user
            )

            user_profile.put()

        #render basic starting page

        self.response.write("<p>Hello: %s %s</p>" % (user_profile.first_name, user_profile.last_name))
        self.response.write("<a href=\"%s\">Logout</a>" % users.create_logout_url("/"))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
