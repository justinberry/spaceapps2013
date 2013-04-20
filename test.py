import webapp2

# Local imports
import annual_solar
import annual_wind
import daily_solar
import location
import utils

class CityLatLng(object):
    def __init__(self, city):
        self.lat = city[0]
        self.lng = city[1]

class Home(webapp2.RequestHandler):

    CITIES = ["Melbourne, VIC",
              "Sydney, NSW",
              "Adelaide, SA",
              "Brisbane, QLD",
              "Canberra, ACT",
              "Darwin, NT",
              "Perth, WA",
              "Alice Springs, NT"]

    def CreateCity(self, city):
        return location.GetLatitudeLongitude(city)

    def get(self):
        cities = {}
        for c in annual_solar.CITY_SOLAR_DATA:
            annual_solar.AnnualSolarPotential(
                key_name=utils.CreateDataStoreKey(c[2], c[3]),
                city=c[0], region=c[1], country="Australia",
                lat=float(c[2]), lng=float(c[3]),
                potential=float(c[4]), actual=float(c[5])).put()
            self.response.out.write("Added %s solar data<br/>" % c[0])
        for c in annual_wind.CITY_WIND_DATA:
            annual_wind.AnnualWindPotential(
                key_name=utils.CreateDataStoreKey(c[2], c[3]),
                city=c[0], region=c[1], country="Australia",
                lat=float(c[2]), lng=float(c[3]),
                potential=float(c[4]), actual=float(c[5])).put()
            self.response.out.write("Added %s wind data<br/>" % c[0])
        self.response.out.write("--------------------<br/>")
        latitude = self.request.get("lat", default_value=-37.814107)
        longitude = self.request.get("lng", default_value=144.963280)

        country, region, city = location.GetLocationParts(latitude, longitude)

        self.response.out.write(
            "You are in %s, %s, %s.<br/>" % (city, region, country))
        
        solar_potential = annual_solar.AnnualSolar(
            latitude, longitude).GetClosestPotential()
        self.response.out.write(
            "The closest solar metropolis is %(city)s, %(region)s, %(country)s. "
            "It can generate %(potential)s kWh of solar power per year. "
            "Currently, it generates %(actual)s kWh per year.<br/>"
            % {"country": solar_potential.country,
               "region": solar_potential.region,
               "city": solar_potential.city,
               "potential": solar_potential.potential,
               "actual": solar_potential.actual})

        wind_potential = annual_wind.AnnualWind(
            latitude, longitude).GetClosestPotential()
        self.response.out.write(
            "The closest wind metropolis is %(city)s, %(region)s, %(country)s "
            "It can generate %(potential)s kWh of wind power per year. "
            "Currently, it generates %(actual)s kWh per year.<br/>"
            % {"country": wind_potential.country,
               "region": wind_potential.region,
               "city": wind_potential.city,
               "potential": wind_potential.potential,
               "actual": wind_potential.actual})
        mj = daily_solar.GetSunExposure(latitude, longitude)
        kwh = mj / 3.6 * 0.2
        self.response.out.write(
            "Your area had solar exposure of %.2f MJ yesterday. "
            " At 20%% efficency that is %.2f kW/h per 1m^2 solar panel."
            % (mj, kwh))

app = webapp2.WSGIApplication([('/test', Home)], debug=True)

