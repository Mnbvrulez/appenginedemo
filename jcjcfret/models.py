from google.appengine.ext import ndb

class UserProfile(ndb.Model):
    user = ndb.UserProperty()
    admin = ndb.BooleanProperty(required=True, default=False)
    first_name = ndb.StringProperty(required=True, default="Anonymous")
    last_name = ndb.StringProperty(required=True, default="User")

#Question
class Question(ndb.Model):
    user_key = ndb.KeyProperty(kind=UserProfile, required=True)

    text = ndb.StringProperty(required=True)
    created_date = ndb.DateTimeProperty(auto_now_add=True, required =True)

    published = ndb.BooleanProperty(required=True, default=False)
    published_date = ndb.DateTimeProperty(required=False)

#Answer
class Answer(ndb.Model):
    question_key = ndb.KeyProperty(kind=Question, required=True)
    user_key = ndb.KeyProperty(kind=UserProfile, required=True)

    text = ndb.StringProperty(required=True)
    comment = ndb.TextProperty(required=False)
    created_date = ndb.DateTimeProperty(auto_now_add=True, required =True)

    number_votes = ndb.ComputedProperty(lambda self: Vote.query().filter(Vote.answer_key==self.key).count())

#Vote
class Vote(ndb.Model):
    user_key = ndb.KeyProperty(kind=UserProfile, required=True)
    question_key = ndb.KeyProperty(kind=Question, required=True)
    answer_key = ndb.KeyProperty(kind=Answer, required=True)

    created_date = ndb.DateTimeProperty(auto_now_add=True, required =True)
