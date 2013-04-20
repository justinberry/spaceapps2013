import webapp2

# Local imports
import annual_solar
import location

class CityLatLng(object):
    def __init__(self, city):
        self.lat = city[0]
        self.lng = city[1]

class Home(webapp2.RequestHandler):

    CITIES = ["San Francisco, CA",
              "Los Angeles, CA",
              "Oakland, CA",
              "Reno, NV",
              "Las Vegas, NV"]

    def CreateCity(self, city):
        return location.GetLatitudeLongitude(city)

    def get(self):
        cities = {}
        for c in self.CITIES:
            cities[c] = self.CreateCity(c)
            self.response.out.write("%s: %s</br>" % (c, cities[c]))
        fs = [CityLatLng(c) for c in cities.itervalues()]
        self.response.out.write(
            location.GetDistances(fs[0].lat, fs[0].lng, fs[1:]))
        self.response.out.write(
            location.GetMinCandidate(fs[0].lat, fs[0].lng, fs[1:]))


app = webapp2.WSGIApplication([('/test', Home)], debug=True)

