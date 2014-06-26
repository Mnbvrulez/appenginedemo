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
import jinja2
import json
import os
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb

import models

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class RedirectHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect("/top")

class MainHandler(webapp2.RequestHandler):
    def get(self, question_filter):

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

        #adjust the questions based on the filter
        questions = models.Question.query()

        if question_filter == "top":
            pass
        elif question_filter == "new":
            questions = questions.filter(models.Question.published==True).order(-models.Question.published_date)
        elif question_filter == "me":
            questions = questions.filter(models.Question.published==True, models.Question.user_key==user_profile.key).order(-models.Question.published_date)
        elif question_filter == "draft":
            questions = questions.filter(models.Question.published==False, models.Question.user_key==user_profile.key).order(-models.Question.created_date)


        template_values = {
            "logout_url": users.create_logout_url("/"),
            "user_profile": user_profile,
            "question_filter": question_filter,
            "questions": questions
        }


        template = JINJA_ENVIRONMENT.get_template('app.html')
        app_markup = template.render(template_values)
        self.response.write(app_markup)

app = webapp2.WSGIApplication([
    ('/', RedirectHandler),
    ('/(top|new|me|draft)', MainHandler),
], debug=True)

class APIHandler(webapp2.RequestHandler):
    
    @property
    def user_profile(self):
        user = users.get_current_user()
        user_profile_key = ndb.Key("UserProfile", user.user_id())

        return user_profile_key.get()


class QuestionHandler(APIHandler):

    def post(self):

        request_body = self.request.body
        request_body_json = json.loads(request_body)

        question = models.Question(
            user_key = self.user_profile.key,
            text = request_body_json["question_text"]
        )
        question.put()

        self.response.write("{\"question_id\": \"%i\"}" % question.key.id())

class QuestionDeleteHandler(APIHandler):

    def delete(self, question_id):
        
        question_key = ndb.Key("Question", int(question_id))
        question = question_key.get()
        if question is None:
            self.response.status = "404 Not Found"
            return

        question_key.delete()

api = webapp2.WSGIApplication([
    ('/api/question', QuestionHandler),
    ('/api/question/([0-9]+)', QuestionDeleteHandler)
], debug=True)

"""
class AnswerHandler(APIHandler):

    def post(self):

        request_body = self.request.body
        request_body_json = json.loads(request_body)

        question = models.Answ(
            user_key = self.user_profile.key,
            text = request_body_json["question_text"]
        )
        question.put()
"""
 
             


