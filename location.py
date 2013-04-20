from google.appengine.api import urlfetch

MAPS_API_TEMPLATE = (
    "http://maps.googleapis.com/maps/api/geocode/json?"
    "latlng=%(latlng)s&sensor=false")


def GetLocationName(latitude, longitude):
    by_country, by_region, by_city = GetLocationParts(latitude, longitude)
    return by_postal_code or by_city or by_country or "Unknown"


def GetLocationParts(latitude, longitude):
    url = MAPS_API_TEMPLATE % {"latlng": "%s,%s" % (latitude, longitude)}
    result = urlfetch.fetch(url)
    location_response = simplejson.loads(result.content)
    by_country = None
    by_region = None
    by_city = None
    for res in location_response["results"]:
        if "city" in res["types"]:
            by_city = res["formatted_address"] 
        elif "administrative_area_level_1" in res["types"]:
            by_region = res["formatted_address"]
        elif "country" in res["types"]:
            by_country = res["formatted_address"]
    return (by_country, by_region, by_city)
