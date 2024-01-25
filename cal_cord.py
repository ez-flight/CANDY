import math
from datetime import date, datetime, timedelta

import numpy
from pyorbital.orbital import astronomy
from sgp4.earth_gravity import wgs84

from calc_gmst_iau_1982 import calc_gmst

#pi =math.pi

## Ellipsoid Parameters as tuples (semi major axis, inverse flattening)
grs80 = (6378137, 298.257222100882711)
#wgs84 = (6378137., 1./298.257223563)
wgs84 = (6378137, 298.257223563)

def dayss(utc_time):
    year = utc_time.year
    month = utc_time.month
    day = utc_time.day
    hour = utc_time.hour
    minute = utc_time.minute
    second = utc_time.second
    dwhole = 367*year-int(7*(year+int((month+9)/12))/4)+int(275*month/9)+day-730531.5
    dfrac = (hour+minute/60+second/3600)/24
    d = dwhole+dfrac
    return d

def days(utc_time):
    year = utc_time.year
    month = utc_time.month
    day = utc_time.day
    hour = utc_time.hour
    minute = utc_time.minute
    second = utc_time.second
    if month < 3:
        year  -= 1
        month += 12
    b = int(year/400)-int(year/100)+int(year/4)
    d = (hour + (minute/60.0) + (second/3600.0))/24.0
    MJD = (365*year) - 679004 + b + int(30.6001*(month+1)) + day + d
    return MJD

def gmsts(utc_time):
    PI2 = math.pi * 2    # => 6.283185307179586
    D2R = math.pi / 180  # => 0.017453292519943295
    jd_ut1 = days(utc_time) # юлианская дата момента наблюдения
 #   print (f"UTC TIME {utc_time}")
 #   print (f"JD(UT1) - {jd_ut1}")
    t_ut1= (jd_ut1 - 2451545.0) / 36525
#    print (f"T промежуток времени в юлианских столетиях {t_ut1}")
    gmst =  67310.54841+ (876600.0 * 3600.0 + 8640184.812866 + (0.093104 - 6.2e-6 * t_ut1) * t_ut1) * t_ut1
    gmst = (gmst * D2R / 240.0) % PI2
    if gmst < 0.0:
        gmst += PI2
    return gmst


def GMST(utc_time): #гринвичское звёздное время
    d = days(utc_time)
    GMST = 280.46061837+360.98564736629*d
    GMST = GMST-360*int(GMST/360)
    if GMST<0:
        GMST = 360.0+GMST
    return GMST*pi/180.0


def ISK_to_GSK(alfa, X_isk,Y_isk,Z_isk): # Перевод из ИСК Гринвеческую СК
    cz = math.cos(alfa) #alfa - гринвичское звёздное время в радианах
    sz = math.sin(alfa)
    Rz = ([
    [cz,sz,0],
    [-sz,cz,0],
    [0,0,1]])
    position = X_isk, Y_isk, Z_isk
    p =  numpy.dot(position,Rz)
    return p [0], p[1], p[2]


def GSK_to_ISK(alfa, X_gsk, Y_gsk, Z_gsk): # Перевод из Гринвеческой СК в инерциальную СК
    cz = math.cos(alfa) #alfa - гринвичское звёздное время в радианах
    sz = math.sin(alfa)
    Rz = ([
    [cz,sz,0],
    [-sz,cz,0],
    [0,0,1]])
    position = X_gsk, Y_gsk, Z_gsk
    Rz_inv = numpy.linalg.inv(Rz)
    p =  numpy.dot(position,Rz_inv)
    return p[0],p[1],p[2]

def geodetic_to_geocentric(latitude, longitude, height, ellipsoid):
    """Возвращает геоцентрические (декартовы) координаты x, y, z соответствующие
    геодезические координаты, заданные по широте и долготе (в
    градусах) и высота над эллипсоидом. Эллипсоид должен быть
    задан парой (большая полуось, взаимное сглаживание).
    """
    φ = math.radians(latitude)
    λ = math.radians(longitude)
    sin_φ = math.sin(φ)
    a, rf = ellipsoid           # большая полуось, взаимное сплющивание
    e2 = 1 - (1 - 1 / rf) ** 2  # квадрат первого эксцентриситета эллипсоида.
    n = a / math.sqrt(1 - e2 * sin_φ ** 2) # основной вертикальный радиус
    r = (n + height) * math.cos(φ)   # перпендикулярное расстояние от оси z
    x = r * math.cos(λ)
    y = r * math.sin(λ)
    z = (n * (1 - e2) + height) * sin_φ
    return x/1000, y/1000, z/1000


def geodetic_to_ISK(latitude, longitude, height, ellipsoid, utc_time):
    X_gsk, Y_gsk, Z_gsk = geodetic_to_geocentric(latitude, longitude, height, ellipsoid)
    pr = math.sqrt((X_gsk**2)+(Y_gsk**2)+(Z_gsk**2))
#    print(f"Проверка на радиус земли {pr}")
#    print(f"X = {X_gsk}, Y = {Y_gsk}, Z = {Z_gsk} ")
    alfa = calc_gmst(utc_time)
    X_isk, Y_isk, Z_isk = GSK_to_ISK(alfa, X_gsk, Y_gsk, Z_gsk)
    return X_isk, Y_isk, Z_isk

def _test():
    lat = 55.75583
    lon = 37.6173
    h = 155
    X_msk = 2849.897965
    Y_msk = 2195.949753
    Z_msk = 5249.076832

    delta = timedelta(days=0, seconds=0.5, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
    dt_start = datetime.utcnow()
    dt_end = dt_start + timedelta(
        days=1,
        seconds=0,
        microseconds=0,
        milliseconds=0,
        minutes=0,
        hours=0,
        weeks=0
    )
    dt = dt_start
    X_isk, Y_isk, Z_isk = geodetic_to_ISK(lat, lon, h, wgs84, dt_start)
    print(f"X = {X_isk}, Y = {Y_isk}, Z = {Z_isk} ")

    while dt<dt_end:
#        if calc_gmst(dt) < 0.0001:
#            print(f"1 -> {calc_gmst(dt)} на {dt}")
#        if astronomy.gmst(dt) < 0.0001:
#            print(f"2 -> {astronomy.gmst(dt)} на {dt}")
#        if GMST(dt) < 0.0001:
#            print(f"3 -> {GMST(dt)} на {dt}")      
#        if gmsts(dt) < 0.0001:
#            print(f"4 -> {gmsts(dt)} на {dt}")

      
#        print (p)
#        print (p_0)
        dt += delta



if __name__ == "__main__":
    _test()
