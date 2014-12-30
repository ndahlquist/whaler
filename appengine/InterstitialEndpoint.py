import logging
import webapp2
from credentials import BASE_URL

from datamodel import OauthEntry


class InterstitialEndpoint(webapp2.RequestHandler):
    """
    Returns a URL that the client should redirect to on pressing the "squash merge" button.
    This may include the URL to authorize the GitHub application, a URL to update the chrome extension,
    or any URL we may need in the future.

    Returns nothing if the user does not need an interstitial.
    """

    def get(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')

        username = self.request.get('username')
        redirect = self.request.get('redirect')
        session_token = self.request.get('session_token')

        oauth = OauthEntry.lookup(username, session_token)

        if oauth is None:
            logging.info('Requesting new oauth token.')
            self.response.text = 'https://github.com/login/oauth/authorize?' + \
                                 'client_id=331e31888360cb8fff32&' + \
                                 'redirect_uri=%s/oauth_callback/%s' % (BASE_URL, username) + \
                                 '&scope=public_repo,repo,write:repo_hook' + \
                                 '&state=%s+%s' % (redirect, session_token)
