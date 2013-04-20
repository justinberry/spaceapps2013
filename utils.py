def CreateDataStoreKey(lat, lng):
    """Currently most of our data store keys are LatLang."""
    return "%s:%s" % (lat, lng)
