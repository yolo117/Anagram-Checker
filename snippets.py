from google.appengine.api import users
from google.appengine.ext import ndb

class MyUser(ndb.Model):
    user = ndb.StringProperty()
    uniqueAnagramCounter = ndb.IntegerProperty()
    wordCounter = ndb.IntegerProperty()

class Words(ndb.Model):
    wordsList = ndb.StringProperty(repeated=True)
    count_of_words = ndb.IntegerProperty()
    alphabet_no_List=ndb.IntegerProperty(repeated=True)
