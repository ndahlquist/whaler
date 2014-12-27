import webapp2


class MainPageEndoint(webapp2.RequestHandler):
    def get(self):
        self.redirect("https://github.com/ndahlquist/whaler")