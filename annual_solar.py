from google.appengine.ext import db

# Local imports
import location

class AnnualSolarPotential(db.Model):
    latitude = db.FloatProperty(required=True)
    longitude = db.FloatProperty(required=True)
    last_updated = db.DateTimeProperty(auto_now=True, auto_now_add=True)


class AnnualSolar(object):
    """Provides data about annual solar capacity at given lat/lang."""
    
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def GetClosestPotential(self):
        """Returns the AnnualSolarPotential from the closest known location."""
        
