from google.appengine.ext import ndb


class OauthEntry(ndb.Model):
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    username = ndb.StringProperty()
    access_token = ndb.StringProperty()
