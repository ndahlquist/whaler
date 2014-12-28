import logging
import webapp2

from datamodel import OauthEntry


class HasOauthEndpoint(webapp2.RequestHandler):
    """
    Returns 'true' if the user has given us oauth access.
    """

    def get(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')

        username = self.request.get('username')
        logging.info("username=%s", username)

        q = OauthEntry.all()
        q.filter("username =", username)
        oauth = q.get()

        self.response.body = 'false' if oauth is None else 'true'