# Импорт модуля math
import math
from datetime import date, datetime

# Ключевой класс библиотеки pyorbital
from pyorbital.orbital import Orbital
from sgp4.api import Satrec
from sgp4.earth_gravity import wgs84

from read_TBF import read_tle_base_file, read_tle_base_internet

s_name, tle_1, tle_2 = read_tle_base_file(25544)
#s_name, tle_1, tle_2 = read_tle_base_internet(25544)
utc_time = datetime.utcnow()
sat = Satrec.twoline2rv(tle_1,tle_2)

R_z=wgs84.radiusearthkm # радиус земли
H_a=sat.alta * R_z # высота апогея
H_p=sat.altp * R_z # высота перегея

u=398600.44158 #геоцентрическая гравитационная постоянная

# Ещё одна простая функция, для демонстрации принципа.
# На вход она потребует две строки tle и время utc в формате datetime.datetime
def get_lat_lon_sgp (tle_1, tle_2, utc_time):
    # Инициализируем экземпляр класса Orbital двумя строками TLE
    orb = Orbital("N", line1=tle_1, line2=tle_2)
    # Вычисляем географические координаты функцией get_lonlatalt, её аргумент - время в UTC.
    lon, lat, alt = orb.get_lonlatalt(utc_time)
    return lon, lat, alt

# Обращаемся к фукнции и выводим результат
lon, lat, alt = get_lat_lon_sgp (tle_1, tle_2, utc_time)

H_0 = alt # высота начала съемки

# вычислим эксестирицент орбиты
#e=(H_a-H_p)/(H_a+H_p+2*R_z)
e = sat.ecco
# Вычислим фокальный параметр орбиты
p=(H_a+R_z)*(1-e)
# Вычислим истинную аномалию
if H_0 < H_p or H_0 > H_a:
    print(f"Бро херня какая то разница между высотой и апогеем ИСЗ {(H_0-H_a):.2f}")
    anom_0 = 0 
else:
    anom_0 = math.acos((p-R_z-H_0)/(e*(R_z+H_0)))

print (f"Расчеты ведутся для {s_name}")
print (f"Эксестирицент орбиты {e}")
print (f"Фокальный параметр орбиты {p:.3f}")
print(f"Apogee:  {H_a}")
print(f"Perigee: {H_p}")
print(f"Высота начала съемки: {H_0}")
print (f"Истинная аномалия {anom_0}")

# Вычислим длительность наблюдения t_s
#t_s= 

