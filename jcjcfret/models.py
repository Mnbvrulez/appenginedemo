from google.appengine.ext import ndb

class UserProfile(ndb.Model):
    user = ndb.UserProperty()
    admin = ndb.BooleanProperty(required=True, default=False)
    first_name = ndb.StringProperty(required=True, default="John")
    last_name = ndb.StringProperty(required=True, default="Doe")

#Question
#Answer
#Vote