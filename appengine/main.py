#!/usr/bin/env python

import webapp2

from InterstitialEndpoint import InterstitialEndpoint
from OauthCallbackEndpoint import OauthCallbackEndpoint
from QueueMergeEndpoint import QueueMergeEndpoint
from MainPageEndpoint import MainPageEndoint


app = webapp2.WSGIApplication([
    ('/interstitial', InterstitialEndpoint),
    (r'/oauth_callback/(.*)', OauthCallbackEndpoint),
    ('/queue_merge', QueueMergeEndpoint),
    ('/', MainPageEndoint),
], debug=True)
