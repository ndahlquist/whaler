#!/usr/bin/env python

import webapp2

from HasOauthEndpoint import HasOauthEndpoint
from OauthCallbackEndpoint import OauthCallbackEndpoint
from QueueMergeEndpoint import QueueMergeEndpoint
from MainPageEndpoint import MainPageEndoint


app = webapp2.WSGIApplication([
    ('/has_oauth', HasOauthEndpoint),
    (r'/oauth_callback/(.*)', OauthCallbackEndpoint),
    ('/queue_merge', QueueMergeEndpoint),
    ('/', MainPageEndoint),
], debug=True)
