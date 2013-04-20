import os
import time
import webapp2
import json

from django.utils import simplejson

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
from StringIO import StringIO

# Local imports
import location

class Home(webapp2.RequestHandler):

    BOM_FEED_URL = "http://www.bom.gov.au/fwo/IDV60701/IDV60701.95964.json"

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

        jsonResponse = self.readFeed(self.BOM_FEED_URL)

        if jsonResponse is None:
            self.response.out.write("Failed fetching data feed from %s" % url)
            return

        self.response.out.write(self.translateBomJsonResponse(jsonResponse))

    # TODO - need to differentiate between feed types and parse accordingly.
    def translateBomJsonResponse(self, rawJson):
        data = rawJson['observations']['data'][0]
        translatedJson = {}
        translatedJson['WindSpeed'] = data['wind_spd_kt']
        # TODO - windspeed is kind of complicated and dependent on the turbine itself and air density.
        # Fudge some constants and maybe try and work out how to use the formula described here:
        # http://www.raeng.org.uk/education/diploma/maths/pdf/exemplars_advanced/23_wind_turbine.pdf
        translatedJson['LastFetch'] = data['local_date_time']
        translatedJson['WindSpeed'] = data['wind_spd_kt']
        translatedJson['WindSpeedEnergy'] = '100kJ'
        translatedJson['Latitude'] = data['lat']
        translatedJson['Longtitude'] = data['lon']
        io = StringIO()
        json.dump(translatedJson, io)
        return io.getvalue()
 
    def readFeed(self, url):
        response = urlfetch.fetch(url)

        if response.status_code == 200:
            jsonResponse = response.content
            return json.loads(jsonResponse)
        else:
            return None


app = webapp2.WSGIApplication([('/', Home)], debug=True)

