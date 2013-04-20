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
        """Returns the AnnualSolarPotential from the closest known location."""
        country, region, city = location.GetLocationParts(
            self.lat, self.lng)
        where_clauses = ["country = %s" % country]
        if region:
            where_clauses.append("region = %s" % region)
        if city:
            where_clauses.append("city = %s" % city)
        query = db.GqlQuery(
            "SELECT lat, lng FROM AnnualSolarPotential WHERE %s"
            % " AND ".join(where_clauses))
        candidates = query.run(limit=100)  # TODO(zhi)
        destinations = [(x.lat, x.lng) for x in candidates]
        
