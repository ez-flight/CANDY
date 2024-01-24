import math
import numpy
from sgp4.earth_gravity import wgs84
from datetime import date, datetime, timedelta

from pyorbital.orbital import astronomy

pi =3.14

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


def ISKtoGSK(utc_time, x,y,z): # Перевод из инерциальной системы в Гринвеческую
    alfa = astronomy.gmst(utc_time)
 #   alfa_2 = gmst(utc_time)
 #   print (f"Угол ={alfa} {alfa_2} в время {utc_time}")
    cz = math.cos(alfa) #alfa - гринвичское звёздное время в радианах
    sz = math.sin(alfa)

    Rz = ([
    [cz,sz,0],
    [-sz,cz,0],
    [0,0,1]])

    position = x,y,z
    p =  numpy.dot(position,Rz)
    return p [0], p[1], p[2]


def GSKtoISK(utc_time, x,y,z): # Перевод из Гринвеческой СК в инерциальную СК
    alfa = astronomy.gmst(utc_time)
    print (f"Угол ={alfa}  в время {utc_time}")
    cz = math.cos(alfa) #alfa - гринвичское звёздное время в радианах
    sz = math.sin(alfa)

    Rz = ([
    [cz,sz,0],
    [-sz,cz,0],
    [0,0,1]])

    position = x,y,z
    Rz_inv = numpy.linalg.inv(Rz)
    p =  numpy.dot(position,Rz_inv)
    return p[0],p[1],p[2]

def _test():

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

    xyz=[-6340.40130292,3070.61774516,684.52263588]
    while dt<dt_end:
       # p = GSKtoISK(dt,xyz[0], xyz[1], xyz[2])
#    print(GMST(dt_start))
 #   print(f"GMST = {gmst(dt_start)}")
        if astronomy.gmst(dt) < 0.0001:
            print(f"1 -> {astronomy.gmst(dt)} на {dt}")
        if gmsts(dt) < 0.0001:
            print(f"2 -> {gmsts(dt)} на {dt}")
        if GMST(dt) < 0.0001:
            print(f"3 -> {GMST(dt)} на {dt}")
#        print (p)
#        print (p_0)
        dt += delta

if __name__ == "__main__":
    _test()
