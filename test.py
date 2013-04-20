import webapp2

# Local imports
import annual_solar
import location

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

    CITY_SOLAR_DATA = [
        ("Adelaide", "South Australia", -34.9286212, 138.5999594, 175, 120),
        ("Alice Springs", "Northern Territory",
         -23.7002104, 133.8806114, 210, 60),
        ("Brisbane", "Queensland", -27.4710107, 153.0234489, 220, 80),
        ("Canberra", "Australian Capital Territory",
         -35.3082355, 149.1242241, 120, 50),
        ("Darwin", "Northern Territory", -12.4628198, 130.8417694, 180, 90),
        ("Perth", "Western Australia", -31.9530044, 115.8574693, 250, 75),
        ("Melbourne", "Victoria", -37.814107, 144.96328, 150, 100),
        ("Sydney", "New South Wales", -33.8674869, 151.2069902, 200, 90),
        ]

    def CreateCity(self, city):
        return location.GetLatitudeLongitude(city)

    def get(self):
        cities = {}
        for c in self.CITY_SOLAR_DATA:
            self.response.out.write("Added %s<br/>" % c[0])
            annual_solar.AnnualSolarPotential(
                key_name="%s,%s" % (c[2], c[3]),
                city=c[0], region=c[1], country="Australia",
                lat=float(c[2]), lng=float(c[3]),
                potential=float(c[4]), actual=float(c[5])).put()
        self.response.out.write("--------------------<br/>")
        latitude = self.request.get("lat", default_value=-37.814107)
        longitude = self.request.get("lng", default_value=144.963280)
        solar_potential = annual_solar.AnnualSolar(latitude, longitude)
        self.response.out.write(
            "(%s, %s) is closest to %s" 
            % (latitude, longitude, solar_potential.GetClosestPotential()))


app = webapp2.WSGIApplication([('/test', Home)], debug=True)

