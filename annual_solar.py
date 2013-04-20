from google.appengine.ext import db

# Local imports
import location


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
