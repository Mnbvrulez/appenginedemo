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
from datetime import datetime

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
             questions = questions.filter(models.Question.published==True)
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
            "questions": questions,
     
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


class QuestionCreate(APIHandler):

    def post(self):

        request_body = self.request.body
        request_body_json = json.loads(request_body)

        question = models.Question(
            user_key = self.user_profile.key,
            text = request_body_json["question_text"]
        )
        question.put()

        self.response.write("{\"question_id\": \"%i\"}" % question.key.id())

class QuestionDelete(APIHandler):

    def delete(self, question_id):
        
        question_key = ndb.Key("Question", int(question_id))
        question = question_key.get()
        if question is None:
            self.response.status = "404 Not Found"
            return

        question_key.delete()


class AnswerCollection(APIHandler):

    def get(self, question_id):

        question_key = ndb.Key("Question", int(question_id))
        question = question_key.get()
        if question is None:
            self.response.status = "404 Not Found"
            return

        answers = models.Answer.query().filter(models.Answer.question_key==question.key)

        #TODO: Order answers by votes

        answer_objects = list()
        for answer in answers:

            answer_object = {
                "answer_id": answer.key.id(),
                "answer_text": answer.text,
                "answer_comment": answer.comment
            }
            answer_objects.append(answer_object)

        self.response.write(json.dumps(answer_objects))

    def post(self, question_id):


        request_body = self.request.body
        request_body_json = json.loads(request_body)

        #check that question exists
        question_key = ndb.Key("Question", int(question_id))
        question = question_key.get()
        if question is None:
            self.response.status = "404 Not Found"
            return

        answer = models.Answer(
            user_key = self.user_profile.key,
            question_key=question.key,
            text = request_body_json["answer_text"],
            comment = request_body_json["answer_comment"]
        )
        answer.put()
        
        self.response.write("{\"answer_id\": \"%i\"}" % answer.key.id())


class QuestionPublish(APIHandler):

    def put(self, question_id):

        question_key = ndb.Key("Question", int(question_id))
        question = question_key.get()
        if question is None:
            self.response.status = "404 Not Found"
            return

        question.published_date = datetime.now()
        question.published = True
        question.put()







api = webapp2.WSGIApplication([
    ('/api/question', QuestionCreate),
    ('/api/question/([0-9]+)', QuestionDelete),
    ('/api/question/([0-9]+)/answer', AnswerCollection),
    ('/api/question/([0-9]+)/publish', QuestionPublish)

], debug=True)
 
             


