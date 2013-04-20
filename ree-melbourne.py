import os
import time
import webapp2

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class Home(webapp2.RequestHandler):

    def get(self):
        latitude = self.request.get("lat", default_value=0)
        longitude = self.request.get("long", default_value=0)
        user_time = self.request.get("t", default_value=time.time())
        self.response.out.write(
            "Your current location is: %s, %s (time: %s)"
            % (latitude, longitude, user_time))


app = webapp2.WSGIApplication([('/', Home)], debug=True)

