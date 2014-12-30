from google.appengine.ext import ndb
import logging


class OauthEntry(ndb.Model):
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    username = ndb.StringProperty()
    access_token = ndb.StringProperty()
    session_token = ndb.StringProperty()

    @classmethod
    def lookup(cls, username, session_token):
        entry = OauthEntry.get_by_id(username)
        if entry is None:
            return None
        if entry.session_token != session_token:
            logging.warning('Session token mismatch: %s vs %s' % (entry.session_token, session_token))
            entry.key.delete()
            return None
        return entry