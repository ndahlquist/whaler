from google.appengine.ext import ndb
import logging


class SessionAuthEntry(ndb.Model):
    """
    This class represents a user's session token.
    Each user should have one or more of these entries, parented by a UserEntry.
    """
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    session_token = ndb.StringProperty()


class UserEntry(ndb.Model):
    """
    This class represents a unique user of the app.
    Each user should have exactly one of these entries.
    """
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    username = ndb.StringProperty()
    oauth_token = ndb.StringProperty()

    @classmethod
    def lookup(cls, username, session_token):
        """
        Lookups a UserEntry with username and session token.
        Returns None if either param cannot be matched.
        """
        oauth_entry = UserEntry.get_by_id(username)
        if oauth_entry is None:
            return None

        session_auth_entries = SessionAuthEntry.query(ancestor=oauth_entry.key).fetch()
        for session_auth_entry in session_auth_entries:
            if session_token == session_auth_entry.session_token:
                return oauth_entry

        logging.warning('No matching session token found: %s' % session_token)
        return None

    @classmethod
    def update(cls, username, oauth_token, session_token):
        """
        Adds session_token to username's UserEntry.
        If no UserEntry exists for username, one will be created.
        """
        oauth_entry = UserEntry.get_by_id(username)
        if oauth_entry is None:
            oauth_entry = UserEntry(id=username, username=username, oauth_token=oauth_token)
            oauth_entry.put()

        session_auth_entry = SessionAuthEntry(id=session_token, session_token=session_token, parent=oauth_entry.key)
        session_auth_entry.put()