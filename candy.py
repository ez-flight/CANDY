# Импорт модуля math
import math
from datetime import date, datetime, timedelta

# Ключевой класс библиотеки pyorbital
from pyorbital.orbital import Orbital
from sgp4.api import Satrec
from sgp4.earth_gravity import wgs84

from cal_cord import geodetic_to_geocentric, fromLatLong
from read_TBF import read_tle_base_file, read_tle_base_internet

#25544 37849
#s_name, tle_1, tle_2 = read_tle_base_file(25544)
s_name, tle_1, tle_2 = read_tle_base_internet(37849)
utc_time = datetime.utcnow()
sat = Satrec.twoline2rv(tle_1,tle_2)

wgs_84 = (6378137., 1./298.257223563)

delta = timedelta(
    days=0,
    seconds=0,
    microseconds=0,
    milliseconds=0,
    minutes=10,
    hours=0,
    weeks=0
)

dt_start = datetime.now()
dt_end = datetime(2024,1,30,10,50,1)
dt = dt_start



R_z=wgs84.radiusearthkm # радиус земли
#R_z= 6378.137
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
    return lon, lat, alt

def get_position (tle_1, tle_2, utc_time):
    # Инициализируем экземпляр класса Orbital двумя строками TLE
    orb = Orbital("N", line1=tle_1, line2=tle_2)
    # Вычисляем географические координаты функцией get_lonlatalt, её аргумент - время в UTC.
    R_s, V_s = orb.get_position(utc_time,False)
    X_s, Y_s, Z_s = R_s
    Vx_s, Vy_s, Vz_s = V_s
    return X_s, Y_s, Z_s, Vx_s, Vy_s, Vz_s

lat = 59.95
lon = 30.316667
h = 12

#X_t, Y_t, Z_t = geodetic_to_geocentric(lat, lon, h, af)
X_t, Y_t, Z_t = fromLatLong(lat, lon, h, wgs_84)
# Обращаемся к фукнции и выводим результат
#lon, lat, alt = get_lat_lon_sgp (tle_1, tle_2, utc_time)
#X_s, Y_s, Z_s, Vx_s, Vy_s, Vz_s =get_position (tle_1, tle_2, utc_time)

#R_n = math.sqrt(((X_s-X_t)**2)+((Y_s-Y_t)**2)+((Z_s-Z_t)**2))

#res1 = math.sqrt((X_s**2)+(Y_s**2)+(Z_s**2))
#res2 = math.sqrt((Vx_s**2)+(Vy_s**2)+(Vz_s**2))

while dt<dt_end:
    X_s, Y_s, Z_s, Vx_s, Vy_s, Vz_s = get_position (tle_1, tle_2, dt)
    R_s = math.sqrt((X_s**2)+(Y_s**2)+(Z_s**2)) 
    X = (X_s-X_t)
    Y = (Y_s-Y_t)
    Z = (Z_s-Z_t)
 #   print(f"X={X}, Y={Y}, Z={Z}")
#    print(f"X_s={X_s}, X_t={X_t}")
    R_n = math.sqrt((X**2)+(Y**2)+(Z**2))
  #  print(f"Наклонная Дальность равна {R_n} в {dt}")
    if R_n < R_z:
#        print(R_n)
 #       print(f"Наклонная Дальность равна {R_n} в {dt}")
        f = math.acos(((R_n**2)+(R_s**2)-(R_z**2))/(2*R_n*R_s))
        print(f"Наклонная Дальность -> {R_n:2f}  Ф -> {f}")
#    else:
#        print("!")
    dt += delta

#print(R_z)
print (X_s, Y_s, Z_s, Vx_s, Vy_s, Vz_s)
#print (res1, res2)