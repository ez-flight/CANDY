# Импорт модуля math
import math
import os
from datetime import date, datetime

import spacetrack.operators as op
from dotenv import load_dotenv
# Ключевой класс библиотеки pyorbital
from pyorbital.orbital import Orbital
from sgp4.api import Satrec
# Главный класс для работы с space-track
from spacetrack import SpaceTrackClient

from read_TBF import read_tle_base_file

tle_1, tle_2 = get_spacetrack_tle(25544, None, None, USERNAME, PASSWORD, True)

line=['0 ISS (ZARYA)',
'1 25544U 98067A   21356.62544795  .00006800  00000-0  13125-3 0  9998',
'2 25544  51.6428 130.9420 0004657 342.5227  11.5462 15.49048823317794']

sat = Satrec.twoline2rv(line[1],line[2])
sat2 = Satrec.twoline2rv(tle_1,tle_2)
print((sat.alta * sat.radiusearthkm), (sat.altp * sat.radiusearthkm))
print((sat2.alta * sat2.radiusearthkm), (sat2.altp * sat2.radiusearthkm))


def get_lat_lon_sgp (tle_1, tle_2, utc_time):
    # Инициализируем экземпляр класса Orbital двумя строками TLE
    orb = Orbital("N", line1=tle_1, line2=tle_2)
    # Вычисляем географические координаты функцией get_lonlatalt, её аргумент - время в UTC.
    lon, lat, alt = orb.get_lonlatalt(utc_time)
    return lon, lat, alt

# Обращаемся к фукнции и выводим результат
lon, lat, alt = get_lat_lon_sgp (tle_1, tle_2, utc_time)
print (lat,lon, alt)