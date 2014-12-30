#!/usr/bin/env python

import webapp2

from SupportsWhalerEndpoint import SupportsWhalerEndpoint
from InterstitialEndpoint import InterstitialEndpoint
from OauthCallbackEndpoint import OauthCallbackEndpoint
from MergeEndpoint import MergeEndpoint
from MainPageEndpoint import MainPageEndoint


app = webapp2.WSGIApplication([
    ('/supports_whaler', SupportsWhalerEndpoint),  # Deprecated
    ('/interstitial', InterstitialEndpoint),
    (r'/oauth_callback/(.*)', OauthCallbackEndpoint),
    ('/merge', MergeEndpoint),
    ('/', MainPageEndoint),
], debug=True)
