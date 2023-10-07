import datetime
import time

from skyfield.api import EarthSatellite, Topos, load

# Путь к файлу с данными
TLE_FILE = "https://celestrak.com/NORAD/elements/active.txt" # DB file to download

SAT_NAME = "SUOMI NPP"

# Загружаем данные
satellites = load.tle(TLE_FILE)

# Находим наш спутник по имени в данных
print("loaded {} sats from {}".format(len(satellites), TLE_FILE))
_sats_by_name = {sat.name: sat for sat in satellites.values()}
satellite = _sats_by_name[SAT_NAME]

ts = load.timescale()
t = ts.now()

# Локация с которой мы наблюдаем
location = Topos('52.173141 N', '44.108612 E')

# Находим азимут и угол над горизонтом
difference = satellite - location
topocentric = difference.at(t)

alt, az, distance = topocentric.altaz()

if alt.degrees > 0:
    print('The ISS is above the horizon')

print(alt)
print(az)
print(int(distance.km), 'km')