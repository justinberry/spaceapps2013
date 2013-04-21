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
import annual_solar
import annual_wind
import solar_exposure
import location
import power_usage
import wind

class Home(webapp2.RequestHandler):

    BOM_FEED_URL = "http://www.bom.gov.au/fwo/IDV60701/IDV60701.95964.json"

    def get(self):
        latitude = self.request.get("lat", default_value=-37.814107)
        longitude = self.request.get("lng", default_value=144.963280)
        debug = self.request.get("debug", default_value=0)
        user_time = self.request.get("t", default_value=time.time())

        if debug:
            self.response.out.write(
                "Your current location is: %s, %s (time: %s).<br/>"
                % (latitude, longitude, user_time))
            self.response.out.write(
                "We think you are in %s<br/><br/>" 
                % location.GetLocationName(latitude, longitude))

        jsonResponse = self.ReadFeed(self.BOM_FEED_URL)

        if jsonResponse is None:
            self.response.out.write("Failed fetching data feed from %s" % url)
            return

        data = []
        data.append(self.TranslateBomWindDataResponse(jsonResponse))
        data.append(self.GetAndTranslateDailySolar(latitude, longitude))
        data.append(self.GetAndTranslateMonthlySolar(latitude, longitude))
        data.append(
            self.GetAndTranslateAnnualPowerUsage(latitude, longitude))
        predicted, actual = self.GetAndTranslateAnnualSolar(latitude, longitude)
        data.extend([predicted, actual])
        predicted, actual = self.GetAndTranslateAnnualWind(latitude, longitude)
        data.extend([predicted, actual])
        data = self._TransformToStrings(data)
        self.response.out.write(json.dumps(data))

    def _TransformToStrings(self, data):
        new_data = []
        for json_obj in data:
            new_obj = {}
            for k, v in json_obj.iteritems():
                new_obj[k] = str(v)
            new_data.append(new_obj)
        return new_data

    # TODO - need to differentiate between feed types and parse accordingly.
    def TranslateBomWindDataResponse(self, rawJson):
        bomData = rawJson['observations']['data'][0]
        translatedJson = {}
        translatedJson['FetchTime'] = bomData['local_date_time']
        translatedJson['LastFetch'] = 'LastFetch'
        translatedJson['WindSpeed'] = bomData['wind_spd_kt']
        translatedJson['Latitude'] = bomData['lat']
        translatedJson['Longtitude'] = bomData['lon']

        pressure_hpa = bomData['press']
        air_temp_c = bomData['air_temp']
        air_speed_kt = bomData['wind_spd_kt']
        translatedJson['WindSpeedEnergy'] = wind.GetEnergyOutput(pressure_hpa, air_temp_c, air_speed_kt)

        return translatedJson

    def GetAndTranslateDailySolar(self, latitude, longitude):
        daily_solar = solar_exposure.DailySolarExposure("solar.daily.grid")
        mj = daily_solar.GetSunExposure(latitude, longitude)
        translatedJson = {}
        translatedJson['FetchTime'] = daily_solar.last_updated
        translatedJson['LastFetch'] = 'LastDay'
        translatedJson['Latitude'] = latitude
        translatedJson['Longtitude'] = longitude
        # Solar panels are roughly 20% efficient.
        translatedJson['SolarEnergy'] = round(mj / 3.6 * 0.2, 2)
        return translatedJson

    def GetAndTranslateMonthlySolar(self, latitude, longitude):
        monthly_solar = solar_exposure.DailySolarExposure("solar.monthly.grid")
        mj = monthly_solar.GetSunExposure(latitude, longitude)
        translatedJson = {}
        translatedJson['FetchTime'] = monthly_solar.last_updated
        translatedJson['LastFetch'] = 'LastMonth'
        translatedJson['Latitude'] = latitude
        translatedJson['Longtitude'] = longitude
        # Solar panels are roughly 20% efficient.
        translatedJson['SolarEnergy'] = round(mj / 3.6 * 0.2, 2)
        return translatedJson

    def GetAndTranslateAnnualPowerUsage(self, latitude, longitude):
        annual_consumption = power_usage.AnnualConsumption(latitude, longitude)
        annual_usage = annual_consumption.PowerUsagePerCapita()
        translatedJson = {}
        translatedJson['FetchTime'] = '2013-01-01'
        translatedJson['LastFetch'] = 'LastYear'
        translatedJson['Latitude'] = latitude
        translatedJson['Longtitude'] = longitude
        # Solar panels are roughly 20% efficient.
        translatedJson['ElectricityUsage'] = round(annual_usage, 2)
        return translatedJson

    def GetAndTranslateAnnualSolar(self, latitude, longitude):
        solar_potential = annual_solar.AnnualSolar(
            latitude, longitude).GetClosestPotential()
        translatedJsonActual = {}
        translatedJsonActual['FetchTime'] = solar_potential.last_updated.strftime("%Y-%m-%d")
        translatedJsonActual['LastFetch'] = 'LastYear'
        translatedJsonActual['Latitude'] = latitude
        translatedJsonActual['Longtitude'] = longitude
        translatedJsonActual['SolarEnergy'] = round(solar_potential.actual, 2)
        translatedJsonPotential = dict(translatedJsonActual)
        translatedJsonPotential['SolarEnergy'] = round(
            solar_potential.potential, 2)
        return translatedJsonPotential, translatedJsonActual

    def GetAndTranslateAnnualWind(self, latitude, longitude):
        wind_potential = annual_wind.AnnualWind(
            latitude, longitude).GetClosestPotential()
        translatedJsonActual = {}
        translatedJsonActual['FetchTime'] = wind_potential.last_updated.strftime("%Y-%m-%d")
        translatedJsonActual['LastFetch'] = 'LastYear'
        translatedJsonActual['Latitude'] = latitude
        translatedJsonActual['Longtitude'] = longitude
        translatedJsonActual['WindEnergy'] = round(wind_potential.actual, 2)
        translatedJsonPotential = dict(translatedJsonActual)
        translatedJsonPotential['WindEnergy'] = round(
            wind_potential.potential, 2)
        return translatedJsonPotential, translatedJsonActual

    def ReadFeed(self, url):
        response = urlfetch.fetch(url)

        if response.status_code == 200:
            jsonResponse = response.content
            return json.loads(jsonResponse)
        else:
            return None


app = webapp2.WSGIApplication([('/', Home)], debug=True)

