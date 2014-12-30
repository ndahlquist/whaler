#!/usr/bin/env python

import webapp2

from SupportsWhalerEndpoint import SupportsWhalerEndpoint
from InterstitialEndpoint import InterstitialEndpoint
from OauthCallbackEndpoint import OauthCallbackEndpoint
from QueueMergeEndpoint import QueueMergeEndpoint
from MainPageEndpoint import MainPageEndoint


app = webapp2.WSGIApplication([
    ('/supports_whaler', SupportsWhalerEndpoint),  # Deprecated
    ('/interstitial', InterstitialEndpoint),
    (r'/oauth_callback/(.*)', OauthCallbackEndpoint),
    ('/queue_merge', QueueMergeEndpoint),
    ('/', MainPageEndoint),
], debug=True)
