# Импорт модуля math
import math
from datetime import date, datetime

# Ключевой класс библиотеки pyorbital
from pyorbital.orbital import Orbital
from sgp4.api import Satrec
from sgp4.earth_gravity import wgs84

from read_TBF import read_tle_base_file, read_tle_base_internet

#s_name, tle_1, tle_2 = read_tle_base_file(25544)
s_name, tle_1, tle_2 = read_tle_base_internet(25544)
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

H_0 = (500,573,788,1126,1548,1982,2330,2495,2500)  # высота начала съемки
Н_1 = (641,922,1317,1747,2122,2382,2496,2428,2382)  #высота конца сьемки
a_0 = (57.6,55.4,49.3,41.1,31.9,22.5,13.3,6.4,6.1)  #отклонения по каналу тангажа начала съемки
a_1 = (53.5,46.2,37.1,27.9,19.2,11.8,6.6,9.8,11.8) #отклонения по каналу тангажа конца съемки
an_0 = (0,25,50,75,100,125,150,175,180) # аномалия в начале съемкм 
an_1 = (34.7,60.9,86.7,111.3,134.0,155.1,175.6,199.3,204.9) # аномалия в конце съемкм 
# вычислим эксестирицент орбиты
#e=(H_a-H_p)/(H_a+H_p+2*R_z)
e = sat.ecco
# Вычислим фокальный параметр орбиты
p=(H_a+R_z)*(1-e)
# Вычислим истинную аномалию
if alt < H_p or alt > H_a:
    print(f"Бро херня какая то разница между высотой и апогеем ИСЗ {(alt-H_a):.2f}")
    anom_0 = 0 
else:
    anom_0 = math.acos((p-R_z-alt)/(e*(R_z+alt)))

print (f"Расчеты ведутся для {s_name}")
print (f"Эксестирицент орбиты {e}")
print (f"Фокальный параметр орбиты {p:.3f}")
print(f"Apogee:  {H_a}")
print(f"Perigee: {H_p}")
print(f"Высота начала съемки: {alt}")
print (f"Истинная аномалия {anom_0}")


# Вычислим длительность наблюдения t_s
#t_s= 

