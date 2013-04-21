import webapp2

# Local imports
import annual_solar
import annual_wind
import solar_exposure
import location
import power_usage
import utils

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

    def CreateCity(self, city):
        return location.GetLatitudeLongitude(city)

    def get(self):
        latitude = self.request.get("lat", default_value=-37.814107)
        longitude = self.request.get("lng", default_value=144.963280)

        country, region, city = location.GetLocationParts(latitude, longitude)

        self.response.out.write(
            "You are in %s, %s, %s.<br/>" % (city, region, country))
        
        solar_potential = annual_solar.AnnualSolar(
            latitude, longitude).GetClosestPotential()
        self.response.out.write(
            "The closest solar metropolis is %(city)s, %(region)s, %(country)s. "
            "It can generate %(potential)s kWh of solar power per year. "
            "Currently, it generates %(actual)s kWh per year.<br/>"
            % {"country": solar_potential.country,
               "region": solar_potential.region,
               "city": solar_potential.city,
               "potential": solar_potential.potential,
               "actual": solar_potential.actual})

        wind_potential = annual_wind.AnnualWind(
            latitude, longitude).GetClosestPotential()
        self.response.out.write(
            "The closest wind metropolis is %(city)s, %(region)s, %(country)s "
            "It can generate %(potential)s kWh of wind power per year. "
            "Currently, it generates %(actual)s kWh per year.<br/>"
            % {"country": wind_potential.country,
               "region": wind_potential.region,
               "city": wind_potential.city,
               "potential": wind_potential.potential,
               "actual": wind_potential.actual})
        daily_solar = solar_exposure.DailySolarExposure("solar.daily.grid")
        mj = daily_solar.GetSunExposure(latitude, longitude)
        kwh = mj / 3.6 * 0.2
        self.response.out.write(
            "Your area had solar exposure of %.2f MJ yesterday. "
            " At 20%% efficency that is %.2f kWh per 1m^2 solar panel.<br/>"
            % (mj, kwh))
        usage = power_usage.AnnualConsumption(latitude, longitude)
        gwh_per_capita = usage.PowerUsagePerCapita(region=region)
        self.response.out.write(
            "In %s, on average, a person uses %.2f kWh per year."
            % (region, gwh_per_capita * 1000.0))


app = webapp2.WSGIApplication([('/test', Home)], debug=True)

