# Импорт модуля math
import math
from datetime import date, datetime

# Ключевой класс библиотеки pyorbital
from pyorbital.orbital import Orbital
from sgp4.api import Satrec
from sgp4.earth_gravity import wgs84

from read_TBF import read_tle_base_file, read_tle_base_internet
from cal_cord import geodetic_to_geocentric

#s_name, tle_1, tle_2 = read_tle_base_file(37849)
s_name, tle_1, tle_2 = read_tle_base_internet(37849)
utc_time = datetime.utcnow()
sat = Satrec.twoline2rv(tle_1,tle_2)

R_z=wgs84.radiusearthkm # радиус земли
#H_a=505#sat.alta * R_z # высота апогея
#H_p=sat.altp * R_z # высота перегея

u=398600.44158 #геоцентрическая гравитационная постоянная

# Ещё одна простая функция, для демонстрации принципа.
# На вход она потребует две строки tle и время utc в формате datetime.datetime
def get_lat_lon_sgp (tle_1, tle_2, utc_time):
    # Инициализируем экземпляр класса Orbital двумя строками TLE
    orb = Orbital("N", line1=tle_1, line2=tle_2)
    # Вычисляем географические координаты функцией get_lonlatalt, её аргумент - время в UTC.
    lon, lat, alt = orb.get_lonlatalt(utc_time)
    one, two = orb.get_position(utc_time,False)
    print (one[1])
    return lon, lat, alt

def get_position (tle_1, tle_2, utc_time):
    # Инициализируем экземпляр класса Orbital двумя строками TLE
    orb = Orbital("N", line1=tle_1, line2=tle_2)
    # Вычисляем географические координаты функцией get_lonlatalt, её аргумент - время в UTC.
    one, two = orb.get_position(utc_time,False)
    return one, two

# Обращаемся к фукнции и выводим результат
#lon, lat, alt = get_lat_lon_sgp (tle_1, tle_2, utc_time)
one,two =get_position (tle_1, tle_2, utc_time)
res1 = math.sqrt((one[0]**2)+(one[1]**2)+(one[2]**2))
res2 = math.sqrt((two[0]**2)+(two[1]**2)+(two[2]**2))
print (res1,res2)