import sys
from django.utils import simplejson

from google.appengine.api import urlfetch


MAPS_API_GEOCODE_TMPL = (
    "http://maps.googleapis.com/maps/api/geocode/json?"
    "latlng=%(latlng)s&sensor=false")

MAPS_API_GEOCODE_NAME_TMPL = (
    "http://maps.googleapis.com/maps/api/geocode/json?"
    "address=%(address)s&sensor=false")

MAPS_API_DISTANCE_TMPL = (
    "http://maps.googleapis.com/maps/api/distancematrix/json?"
    "origins=%(origins)s&destinations=%(destinations)s&sensor=false")


def GetDistances(lat, lng, candidates):
    """Distances from a given lat/long to a list of candidate (lat/long).

    Args:
      lat: Latitude, float.
      lng: Longitude, float.
      candidates:  List of objects with a .lat and .lng attribute.
    
    Returns:
      A list of distances (int) indexed 
    """
    url = MAPS_API_DISTANCE_TMPL % {
        "origins": "%s,%s" % (lat, lng),
        "destinations": "|".join(
            ["%s,%s" % (c.lat, c.lng) for c in candidates])
        }
    result = urlfetch.fetch(url)
    distance_response = simplejson.loads(result.content)
    distances = [
        d["distance"]["value"] for d in distance_response["rows"][0]["elements"]]
    return distances


def GetMinCandidate(lat, lng, candidates):
    """From a list of candidates, return the one closest to the given lat/lng.

    Args:
      lat: Latitude, float.
      lng: Longitude, float.
      candidates:  List of objects with a .lat and .lng attribute.
    
    Returns:
      A (lat, lng) of the location closest to the given lat/lng.
    """
    distances = GetDistances(lat, lng, candidates)
    min_distance = sys.maxint
    min_idx = -1
    for i, d in enumerate(distances):
        print i, d
        if d < min_distance:
            min_distance = d
            min_idx = i
    print min_idx
    print candidates
    return candidates[min_idx].lat, candidates[min_idx].lng


def GetLocationName(lat, lng):
    by_country, by_region, by_city = GetLocationParts(lat, lng)
    return by_city or by_region or by_country or "Unknown"


def GetLocationParts(lat, lng):
    url = MAPS_API_GEOCODE_TMPL % {"latlng": "%s,%s" % (lat, lng)}
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


def GetLatitudeLongitude(common_name):
    "Return lat/long for a given common name."
    url = MAPS_API_GEOCODE_NAME_TMPL % {
        "address": common_name.replace(" ", "+")}
    result = urlfetch.fetch(url)
    location_response = simplejson.loads(result.content)
    location = location_response["results"][0]["geometry"]["location"]
    return location["lat"], location["lng"]
