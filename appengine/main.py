#!/usr/bin/env python

import webapp2

from InterstitialEndpoint import InterstitialEndpoint
from PreMergeEndpoint import PreMergeEndpoint
from OauthCallbackEndpoint import OauthCallbackEndpoint
from MergeEndpoint import MergeEndpoint
from ErrorLogEndpoint import ErrorLogEndpoint
from MainPageEndpoint import MainPageEndoint


app = webapp2.WSGIApplication([
    ('/interstitial', InterstitialEndpoint),  # Deprecated 3-29-15
    ('/premerge', PreMergeEndpoint),
    (r'/oauth_callback/(.*)', OauthCallbackEndpoint),
    ('/merge', MergeEndpoint),
    ('/errorlog', ErrorLogEndpoint),
    ('/', MainPageEndoint),
], debug=True)
