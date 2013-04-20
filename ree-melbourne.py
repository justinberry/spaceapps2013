import os
import time
import webapp2

from django.utils import simplejson

from google.appengine.api import urlfetch
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template

MAPS_API_TEMPLATE = (
    "http://maps.googleapis.com/maps/api/geocode/json?"
    "latlng=%(latlng)s&sensor=false")

class Home(webapp2.RequestHandler):

    def GetLocation(self, latitude, longitude):
        url = MAPS_API_TEMPLATE % {"latlng": "%s,%s" % (latitude, longitude)}
        result = urlfetch.fetch(url)
        location_response = simplejson.loads(result.content)
        by_postal_code = None
        by_locality = None
        by_country = None
        for res in location_response["results"]:
            if "postal_code" in res["types"]:
                by_postal_code = res["formatted_address"] 
            elif "locality" in res["types"]:
                by_locality = res["formatted_address"] 
            elif "country" in res["types"]:
                by_country = res["formatted_address"] 
        return by_postal_code or by_locality or by_country or "Unknown"

    def get(self):
        latitude = self.request.get("lat", default_value=-37.814107)
        longitude = self.request.get("long", default_value=144.963280)
        user_time = self.request.get("t", default_value=time.time())

        self.response.out.write(
            "Your current location is: %s, %s (time: %s).<br/>"
            % (latitude, longitude, user_time))

        self.response.out.write(
            "We think you are in %s<br/>" % self.GetLocation(
                latitude, longitude))



app = webapp2.WSGIApplication([('/', Home)], debug=True)

