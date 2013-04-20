import os
import time
import webapp2

from django.utils import simplejson

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template

# Local imports
import location


class Home(webapp2.RequestHandler):

    def get(self):
        latitude = self.request.get("lat", default_value=-37.814107)
        longitude = self.request.get("long", default_value=144.963280)
        user_time = self.request.get("t", default_value=time.time())

        self.response.out.write(
            "Your current location is: %s, %s (time: %s).<br/>"
            % (latitude, longitude, user_time))

        self.response.out.write(
            "We think you are in %s<br/>" 
            % location.GetLocationName(latitude, longitude))



app = webapp2.WSGIApplication([('/', Home)], debug=True)

