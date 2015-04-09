
import webapp2
import logging

from google.appengine.api import urlfetch

from credentials import GITHUB_APP_CLIENT_ID, GITHUB_APP_CLIENT_SECRET
from datamodel import UserEntry


class OauthCallbackEndpoint(webapp2.RequestHandler):
    """
    This is the Oauth callback described at https://developer.github.com/v3/oauth/.
    It takes the temporary token from GitHub, and sends it along with our secret
    to get an application access token.
    """

    def get(self, username):
        try:
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

            UserEntry.update(username=username, oauth_token=result_dict['access_token'],
                                            session_token=session_token)

            self.redirect(referrer)
        except:
            logging.info(repr(self.request))
            raise


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

