# Импорт модуля math
import math
from datetime import datetime, date
# Ключевой класс библиотеки pyorbital
from pyorbital.orbital import Orbital
 
tle_1 = '1 37849U 11061A   23279.05498059  .00000257  00000-0  14269-3 0  9992'
tle_2 = '2 37849  98.7110 215.9136 0000851  62.3990  66.3207 14.19576225618662'
# Нас интересует текущий момент времени
utc_time = datetime.utcnow()

H_a=305000 # высота апогея
H_p=293000 # высота перегея
H_0=293000 # высота начала съемки
R_z=6371.210 # радиус земли
u=398600.44158 #геоцентрическая гравитационная постоянная

# Ещё одна простая функция, для демонстрации принципа.
# На вход она потребует две строки tle и время utc в формате datetime.datetime
def get_lat_lon_sgp (tle_1, tle_2, utc_time):
    # Инициализируем экземпляр класса Orbital двумя строками TLE
    orb = Orbital("N", line1=tle_1, line2=tle_2)
    # Вычисляем географические координаты функцией get_lonlatalt, её аргумент - время в UTC.
    lon, lat, alt = orb.get_lonlatalt(utc_time)
    print (orb.get_position(utc_time))
    return lon, lat, alt

# Обращаемся к фукнции и выводим результат
lon, lat, alt = get_lat_lon_sgp (tle_1, tle_2, utc_time)
print (lon, lat, alt)

# вычислим эксестирицент орбиты
e=(H_a-H_p)/(H_a+H_p+2*R_z)
# Вычислим фокальный параметр орбиты
p=(H_a+R_z)*(1-e)
# Вычислим истинную аномалию
anom_0=math.acos((p-R_z-H_0)/(e*(R_z+H_0)))

#print ("Расчеты ведутся для Suomi NPP")
#print (f"Эксестирицент орбиты {e:.3f}")
#print (f"Фокальный параметр орбиты {p:.3f}")
#print (f"Истинная аномалия {anom_0}")

# Вычислим длительность наблюдения t_s
#t_s= 

