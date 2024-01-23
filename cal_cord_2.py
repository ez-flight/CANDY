import math
import numpy
from sgp4.earth_gravity import wgs84
from datetime import date, datetime, timedelta


pi =3.14

def days(utc_time):
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

def GMST(utc_time): #гринвичское звёздное время
    d = days(utc_time)
    print (d)
    GMST = 280.46061837+360.98564736629*d
    GMST = GMST-360*int(GMST/360)
    if GMST<0:
        GMST = 360.0+GMST
    return GMST


def ISKtoGSK(utc_time, x,y,z): # Перевод из инерциальной системы в Гринвеческую
    alfa = GMST(utc_time)*pi/180.0
    print (f"Угол ={alfa} в время {utc_time}")
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
    alfa = GMST(utc_time)*pi/180.0 #alfa - гринвичское звёздное время в радианах
    print (f"Угол ={alfa} в время {utc_time}")

    cz = math.cos(alfa) 
    sz = math.sin(alfa)

    Rz = ([
    [cz,sz,0],
    [-sz,cz,0],
    [0,0,1]])

    position = x,y,z
 #   A = np.matrix('1 -3; 2 5')
    Rz_inv = numpy.linalg.inv(Rz)
 #   Rz_0 = numpy.array(Rz)
    p =  numpy.dot(position,Rz_inv)
    return p[0],p[1],p[2]

def _test():

    delta = timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=1, weeks=0)
    dt_start = datetime.now()
    dt_end = dt_start + timedelta(
        days=2,
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
        p = ISKtoGSK(dt,xyz[0], xyz[1], xyz[2])
#        print (p)
#        print (p_0)
        dt += delta

if __name__ == "__main__":
    _test()
