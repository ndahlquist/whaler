import webapp2
import os
from google.appengine.ext.webapp import template

class MainPageEndoint(webapp2.RequestHandler):
    def get(self):
        #greetings_query = Greeting.all().order('-date')
        #greetings = greetings_query.fetch(10)

        #if users.get_current_user():
        #    url = users.create_logout_url(self.request.uri)
        #    url_linktext = 'Logout'
        #else:
        #    url = users.create_login_url(self.request.uri)
        #    url_linktext = 'Login'

        template_values = {
            'greetings': ['thing 1', 'thing 2', 'thing 3'],
            'url': 'test url',
            'url_linktext': 'test url link text',
        }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))