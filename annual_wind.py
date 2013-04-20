from google.appengine.ext import db

# Local imports
import location

CITY_WIND_DATA = [
    ("Adelaide", "South Australia", -34.9286212, 138.5999594, 200, 100),
    ("Alice Springs", "Northern Territory",
     -23.7002104, 133.8806114, 110, 60),
    ("Brisbane", "Queensland", -27.4710107, 153.0234489, 80, 0),
    ("Canberra", "Australian Capital Territory",
     -35.3082355, 149.1242241, 250, 50),
    ("Darwin", "Northern Territory", -12.4628198, 130.8417694, 80, 10),
    ("Perth", "Western Australia", -31.9530044, 115.8574693, 50, 15),
    ("Melbourne", "Victoria", -37.814107, 144.96328, 200, 120),
    ("Sydney", "New South Wales", -33.8674869, 151.2069902, 100, 10),
    ]

class AnnualWindPotential(db.Model):
    lat = db.FloatProperty(required=True)
    lng = db.FloatProperty(required=True)
    last_updated = db.DateTimeProperty(auto_now=True, auto_now_add=True)
    country = db.StringProperty()
    region = db.StringProperty()
    city = db.StringProperty()
    potential = db.FloatProperty()
    actual = db.FloatProperty()


class AnnualWind(object):
    """Provides data about annual wind capacity at given lat/lang."""

    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def GetClosestPotential(self):
        """Get the city and potential wind power from the closest location.

        Returns:
          An AnnualWindPotential object.
        """
        country, region, city = location.GetLocationParts(self.lat, self.lng)
        query = db.GqlQuery(
            "SELECT * FROM AnnualWindPotential WHERE country = :1 "
            "  AND region = :2", country, region)
        candidates = query.fetch(100)  # TODO(zhi)
        min_idx = location.GetMinCandidateIndex(self.lat, self.lng, candidates)
        return candidates[min_idx]
        
