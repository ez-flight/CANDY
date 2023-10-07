import math
from datetime import date, datetime

from pyorbital.orbital import Orbital
from sgp4.api import Satrec
from sgp4.earth_gravity import wgs84
from tletools import TLE

tle_string = """
SUOMI NPP
1 37849U 11061A   23280.08921149  .00000269  00000-0  14837-3 0  9992
2 37849  98.7111 216.9310 0000832  62.3537 308.8007 14.19576889618819
"""
# Нас интересует текущий момент времени
utc_time = datetime.utcnow()


tle_lines = tle_string.strip().splitlines()
tle = TLE.from_lines(*tle_lines)

s_name , tle_1, tle_2 = tle_string.strip().splitlines()
# Ещё одна простая функция, для демонстрации принципа.
# На вход она потребует две строки tle и время utc в формате datetime.datetime
def get_lat_lon_sgp(tle_1, tle_2, utc_time):
    # Инициализируем экземпляр класса Orbital двумя строками TLE
    orb = Orbital("N", line1=tle_1, line2=tle_2)
    # Вычисляем географические координаты функцией get_lonlatalt, её аргумент - время в UTC.
    lon, lat, alt = orb.get_lonlatalt(utc_time)
    return lon, lat, alt

# Обращаемся к фукнции и выводим результат
lon, lat, alt = get_lat_lon_sgp(tle_1, tle_2, utc_time)
print (f"Расчеты ведутся для КА {tle.name}")
print(lon, lat, alt)

sat = Satrec.twoline2rv(tle_lines[1],tle_lines[2])

H_a = sat.alta * wgs84.radiusearthkm
H_p = sat.altp * wgs84.radiusearthkm
R_z = wgs84.radiusearthkm # 6371.210  # радиус земли
u = 398600.44158  # геоцентрическая гравитационная постоянная
e = tle.ecc # вычислим эксестирицент орбиты


# Вычислим фокальный параметр орбиты
p = (H_a + R_z) * (1 - e)
# Вычислим истинную аномалию
#anom_0 = math.acos((p - R_z - alt) / (e * (R_z + alt)))

print (f"Эксестирицент орбиты {e:.7f}")
print (f"Фокальный параметр орбиты {p:.3f}")

#print(tle.ecc)
print(H_a-alt)

print((sat.alta * sat.radiusearthkm), (sat.altp * sat.radiusearthkm))