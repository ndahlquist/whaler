
import webapp2
import logging

from google.appengine.api import urlfetch

from credentials import GITHUB_APP_CLIENT_ID, GITHUB_APP_CLIENT_SECRET
from datamodel import OauthEntry


class OauthCallbackEndpoint(webapp2.RequestHandler):
    """
    This is the Oauth callback described at https://developer.github.com/v3/oauth/.
    It takes the temporary token from GitHub, and sends it along with our secret
    to get an application access token.
    """

    def get(self, username):

        code = self.request.get('code')
        referrer = str(self.request.get('state'))

        q = OauthEntry.all()
        q.filter("username =", username)
        oauth = q.get()
        if oauth is not None:
            self.redirect(referrer)
            return

        token_url = "https://github.com/login/oauth/access_token?" + \
                    "client_id=%s&" % GITHUB_APP_CLIENT_ID + \
                    "client_secret=%s&" % GITHUB_APP_CLIENT_SECRET + \
                    "code=%s&" % code

        result = urlfetch.fetch(token_url, method=urlfetch.POST)
        logging.info(result.content)
        result_dict = parse_form_encoded_body(result.content)

        oauth_entry = OauthEntry()
        oauth_entry.username = username
        oauth_entry.access_token = result_dict['access_token']
        oauth_entry.put()

        self.redirect(referrer)


def parse_form_encoded_body(form):
    """
    Parses a form-encoded body into a dictionary.
    """
    dict = {}

    fields = form.split('&')
    for field in fields:
        key_value = field.split('=')
        key = key_value[0]
        value = None if len(key_value) == 1 else key_value[1]
        dict[key] = value

    return dict

