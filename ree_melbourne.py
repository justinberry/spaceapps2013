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
import wind

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

        jsonResponse = self.ReadFeed(self.BOM_FEED_URL)

        if jsonResponse is None:
            self.response.out.write("Failed fetching data feed from %s" % url)
            return

        data = []
        data.append(self.TranslateBomWindDataResponse(jsonResponse))
        self.response.out.write(json.dumps(data))

    # TODO - need to differentiate between feed types and parse accordingly.
    def TranslateBomWindDataResponse(self, rawJson):
        bomData = rawJson['observations']['data'][0]
        translatedJson = {}
        translatedJson['FetchTime'] = bomData['local_date_time']
        translatedJson['LastFetch'] = 'LastFetch'
        translatedJson['WindSpeed'] = bomData['wind_spd_kt']
        translatedJson['Latitude'] = bomData['lat']
        translatedJson['Longtitude'] = bomData['lon']

        pressure_hpa = data['press']
        air_temp_c = data['air_temp']
        air_speed_kt = data['wind_spd_kt']
        translatedJson['WindSpeedEnergy'] = wind.GetEnergyOutput(pressure_hpa, air_temp_c, air_speed_kt)

        return translatedJson
 
    def ReadFeed(self, url):
        response = urlfetch.fetch(url)

        if response.status_code == 200:
            jsonResponse = response.content
            return json.loads(jsonResponse)
        else:
            return None


app = webapp2.WSGIApplication([('/', Home)], debug=True)

