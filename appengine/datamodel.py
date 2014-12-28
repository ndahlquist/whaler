from google.appengine.ext import db


class OauthEntry(db.Model):
    timestamp = db.DateTimeProperty(auto_now_add=True)
    username = db.StringProperty()
    access_token = db.StringProperty()
