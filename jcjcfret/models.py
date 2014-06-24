from google.appengine.ext import ndb

class UserProfile(ndb.Model):
    user = ndb.UserProperty()
    admin = ndb.BooleanProperty(required=True, default=False)
    first_name = ndb.StringProperty(required=True, default="John")
    last_name = ndb.StringProperty(required=True, default="Doe")

#Question
class Question(ndb.Model):
    text = ndb.StringProperty(required=True, default="")
    key = user
    date = ndb.auto_now_add(required =True)

#Answer
class Answer(ndb.Model):
    text = ndb.StringProperty(required=True, default = "")
    key = user
    date = ndb.auto_now_add(required=True)

#Vote
class Vote(ndb.Model):
    key = user
    number = ndb.IntegerProperty(required = True, default =0) 
