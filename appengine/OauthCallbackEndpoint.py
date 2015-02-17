
import webapp2
import logging

from google.appengine.api import urlfetch

from credentials_dev import GITHUB_APP_CLIENT_ID, GITHUB_APP_CLIENT_SECRET
from datamodel import OauthEntry


class OauthCallbackEndpoint(webapp2.RequestHandler):
    """
    This is the Oauth callback described at https://developer.github.com/v3/oauth/.
    It takes the temporary token from GitHub, and sends it along with our secret
    to get an application access token.
    """

    def get(self, username):

        code = self.request.get('code')
        state = str(self.request.get('state')).split(' ')
        referrer = state[0]
        session_token = state[1]

        token_url = "https://github.com/login/oauth/access_token?" + \
                    "client_id=%s&" % GITHUB_APP_CLIENT_ID + \
                    "client_secret=%s&" % GITHUB_APP_CLIENT_SECRET + \
                    "code=%s&" % code

        result = urlfetch.fetch(token_url, method=urlfetch.POST)
        result_dict = parse_form_encoded_body(result.content)

        oauth_entry = OauthEntry(id=username, username=username,
                                 access_token=result_dict['access_token'], session_token=session_token)
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

