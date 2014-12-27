#!/usr/bin/env python

import webapp2

from SupportsWhalerEndpoint import SupportsWhalerEndpoint
from QueueMergeEndpoint import QueueMergeEndpoint
from MainPageEndpoint import MainPageEndoint


app = webapp2.WSGIApplication([
    ('/supports_whaler', SupportsWhalerEndpoint),
    ('/queue_merge', QueueMergeEndpoint),
    ('/', MainPageEndoint),
], debug=True)
