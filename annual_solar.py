from google.appengine.ext import db

# Local imports
import location

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

class AnnualSolarPotential(db.Model):
    lat = db.FloatProperty(required=True)
    lng = db.FloatProperty(required=True)
    last_updated = db.DateTimeProperty(auto_now=True, auto_now_add=True)
    country = db.StringProperty()
    region = db.StringProperty()
    city = db.StringProperty()
    potential = db.FloatProperty()
    actual = db.FloatProperty()


class AnnualSolar(object):
    """Provides data about annual solar capacity at given lat/lang."""

    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def GetClosestPotential(self):
        """Get the city and potential solar power from the closest location.

        Returns:
          An AnnualSolarPotential object.
        """
        country, region, city = location.GetLocationParts(self.lat, self.lng)
        query = db.GqlQuery(
            "SELECT * FROM AnnualSolarPotential WHERE country = :1 "
            "  AND region = :2", country, region)
        candidates = query.fetch(100)  # TODO(zhi)
        min_idx = location.GetMinCandidateIndex(self.lat, self.lng, candidates)
        return candidates[min_idx]
