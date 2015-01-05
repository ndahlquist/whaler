#!/usr/bin/env python

import webapp2

from InterstitialEndpoint import InterstitialEndpoint
from OauthCallbackEndpoint import OauthCallbackEndpoint
from MergeEndpoint import MergeEndpoint
from MainPageEndpoint import MainPageEndoint


app = webapp2.WSGIApplication([
    ('/interstitial', InterstitialEndpoint),
    (r'/oauth_callback/(.*)', OauthCallbackEndpoint),
    ('/merge', MergeEndpoint),
    ('/', MainPageEndoint),
], debug=True)
