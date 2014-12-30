import webapp2


class SupportsWhalerEndpoint(webapp2.RequestHandler):
    """
    Deprecated 12/29/14. Should just return an error message telling user to update.
    """

    def get(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')

        url = "https://chrome.google.com/webstore/detail/whaler/kjfaikbmbbkbnjjeiambmjchclpfkedf"
        self.response.body = "This version of Whaler is now deprecated. " \
                             "Please <a href=\"%s\">update Whaler</a>." % url
