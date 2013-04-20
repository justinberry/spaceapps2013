import math

SPECIFIC_GAS_CONSTANT_DRY_AIR = 287.05 # J/(kg K) in SI units
#AVG_BLADE_LENGTH = 32.5 # Metres
AVG_BLADE_LENGTH = 52 # Metres
BETZ_LIMIT = 0.4

def GetEnergyOutput(pressure_hpa, temp_celsius, air_speed_kt):
    air_speed_m_s = air_speed_kt * 0.514 # m/s - https://en.wikipedia.org/wiki/Knot_(unit)
    return 0.5 * GetRho(pressure_hpa, temp_celsius) * GetSweepArea() * (air_speed_m_s * air_speed_m_s * air_speed_m_s) * BETZ_LIMIT

# aka air density in kg/m^3
def GetRho(pressure_hpa, temp_celsius):
    abs_temp_k = temp_celsius + 273.15
    pressure_pa = pressure_hpa * 100
    return pressure_pa / (SPECIFIC_GAS_CONSTANT_DRY_AIR * abs_temp_k)

def GetSweepArea():
    return math.pi * (AVG_BLADE_LENGTH * AVG_BLADE_LENGTH)

if __name__ == "__main__":
    print "A = %f" % GetSweepArea()
    print "Rho = %f" % GetRho(1023.6, 14)
    print "E = %f Watt hour" % GetEnergyOutput(1023.6, 14, 10)
    print "E = %f kWh" % (GetEnergyOutput(1023.6, 14, 10) / 1000)
    print "E = %f kW a year" % (GetEnergyOutput(1023.6, 14, 10) * 8750 / 1000)
    print "E = %f MW" % (GetEnergyOutput(1023.6, 14, 10) / 1000 / 1000)
