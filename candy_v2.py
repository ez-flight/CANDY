import math
from datetime import date, datetime, timedelta

import numpy as np
import pyorbital
import shapefile
from pyorbital.orbital import XKMPER, F, Orbital
from sgp4.api import Satrec

from read_TBF import read_tle_base_file, read_tle_base_internet

#25544 37849
#s_name, tle_1, tle_2 = read_tle_base_file(37849)
#40420 барс М
# https://www.n2yo.com/satellite/?s=40420
# https://isstracker.pl/en/satelity/40420/godziny-przelotow?lat=59.8983&lng=30.2618
#s_name, tle_1, tle_2 = read_tle_base_internet(40420)
s_name, tle_1, tle_2 = read_tle_base_file(40420)
sat = Satrec.twoline2rv(tle_1, tle_2)

A = 6378.137  # WGS84 Equatorial radius (km)
B = 6356.752314245 # km, WGS84
MFACTOR = 7.292115E-5


def get_xyzv_from_latlon(time, lon, lat, alt):
    """Calculate observer ECI position.
        http://celestrak.com/columns/v02n03/
    """
    lon = np.deg2rad(lon)
    lat = np.deg2rad(lat)

    theta = (pyorbital.astronomy.gmst(time) + lon) % (2 * np.pi)
    c = 1 / np.sqrt(1 + F * (F - 2) * np.sin(lat)**2)
    sq = c * (1 - F)**2

    achcp = (A * c + alt) * np.cos(lat)
    x = achcp * np.cos(theta)  # kilometers
    y = achcp * np.sin(theta)
    z = (A * sq + alt) * np.sin(lat)

    vx = -MFACTOR * y  # kilometers/second
    vy = MFACTOR * x
    vz = 0

    return (x, y, z), (vx, vy, vz)


def get_lonlatalt(pos, utc_time):
    """Calculate sublon, sublat and altitude of satellite, considering the earth an ellipsoid.
    http://celestrak.com/columns/v02n03/
    """
    (pos_x, pos_y, pos_z) = pos / XKMPER
    lon = ((np.arctan2(pos_y * XKMPER, pos_x * XKMPER) - astronomy.gmst(utc_time)) % (2 * np.pi))
    lon = np.where(lon > np.pi, lon - np.pi * 2, lon)
    lon = np.where(lon <= -np.pi, lon + np.pi * 2, lon)

    r = np.sqrt(pos_x ** 2 + pos_y ** 2)
    lat = np.arctan2(pos_z, r)
    e2 = F * (2 - F)
    while True:
        lat2 = lat
        c = 1 / (np.sqrt(1 - e2 * (np.sin(lat2) ** 2)))
        lat = np.arctan2(pos_z + c * e2 * np.sin(lat2), r)
        if np.all(abs(lat - lat2) < 1e-10):
            break
    alt = r / np.cos(lat) - c
    alt *= A
    return np.rad2deg(lon), np.rad2deg(lat), alt


def get_lat_lon_sgp(tle_1, tle_2, utc_time):
    # Инициализируем экземпляр класса Orbital двумя строками TLE
    orb = Orbital("N", line1=tle_1, line2=tle_2)
    # Вычисляем географические координаты функцией get_lonlatalt, её аргумент - время в UTC.
    lon, lat, alt = orb.get_lonlatalt(utc_time)
    return lon, lat, alt

def get_position(tle_1, tle_2, utc_time):
    # Инициализируем экземпляр класса Orbital двумя строками TLE
    orb = Orbital("N", line1=tle_1, line2=tle_2)
    # Вычисляем геоцентрические координаты функцией get_position
    R_s, V_s = orb.get_position(utc_time, False)
    X_s, Y_s, Z_s = R_s
    Vx_s, Vy_s, Vz_s = V_s
    return X_s, Y_s, Z_s, Vx_s, Vy_s, Vz_s

def create_orbital_track_shapefile_for_day(tle_1, tle_2, dt_start, output_shapefile):

    dt = dt_start

    #Координаты объекта в геодезической СК
    lat_t = 59.95  
    lon_t = 30.316667 
    alt_t = 12

    #Задаем шаг по времени для прогноза
    delta = timedelta(
        days=0,
        seconds=10,
        microseconds=0,
        milliseconds=0,
        minutes=0,
        hours=0,
        weeks=0
    ) 
    #Задаем конец времени прогноза
    dt_end = dt_start + timedelta(
        days=1,
        seconds=0,
        microseconds=0,
        milliseconds=0,
        minutes=0,
        hours=0,
        weeks=0
    )
    
    # Создаём экземляр класса Orbital
    orb = Orbital("N", line1=tle_1, line2=tle_2)

    # Создаём экземпляр класса Writer для создания шейп-файла, указываем тип геометрии
    track_shape = shapefile.Writer(output_shapefile, shapefile.POINT)

    # Добавляем поля - идентификатор, время, широту и долготу
    # N - целочисленный тип, C - строка, F - вещественное число
    # Для времени придётся использовать строку, т.к. нет поддержки формата "дата и время"
    track_shape.field("ID", "N", 40)
    track_shape.field("TIME", "C", 40)
    track_shape.field("LON", "F", 40)
    track_shape.field("LAT", "F", 40)
    track_shape.field("R_s", "F", 40)
    track_shape.field("R_t", "F", 40)
    track_shape.field("R_n", "F", 40)
    track_shape.field("Ф", "F", 40)

    # Объявляем счётчики, i для идентификаторов, minutes для времени
    i = 0

    while dt < dt_end:
        # Считаем положение спутника в инерциальной СК
        X_s, Y_s, Z_s, Vx_s, Vy_s, Vz_s = get_position (tle_1, tle_2, dt)

        # Считаем положение спутника в геодезической СК
        lon_s, lat_s, alt_s = get_lat_lon_sgp(tle_1, tle_2, dt)
        
        #проверка обратно в геодезическую
        #pos = np.array((X_s,Y_s,Z_s))
        #lon,lat,alt= get_lonlatalt(pos, dt)
        #print(lon_s, lon, lat_s, lat,alt_s, alt )

        #проверка обратно в инерциальную
        #pos2, v2 = get_xyzv_from_latlon(dt, lon, lat, alt)
        #print(pos, pos2)

        #Длина вектора положения и вектора скорости КА 
        R_s = math.sqrt((X_s**2)+(Y_s**2)+(Z_s**2))
        V_s = math.sqrt((Vx_s**2)+(Vy_s**2)+(Vz_s**2))
        
        #Персчитываем положение объекта из геодезической в инерциальную СК  на текущее время с расчетом компонентов скорости точки на земле
        pos_t, v_t = get_xyzv_from_latlon(dt, lon_t, lat_t, alt_t)
        X_t = pos_t[0]
        Y_t = pos_t[1]
        Z_t = pos_t[2]        
        Vx_t = v_t[0]
        Vy_t = v_t[1]
        Vz_t = v_t[2]        
        R_t = math.sqrt((X_t**2)+(Y_t**2)+(Z_t**2))
        V_t = math.sqrt((Vx_t**2)+(Vy_t**2)+(Vz_t**2))

        X = (X_s-X_t)
        Y = (Y_s-Y_t)
        Z = (Z_s-Z_t)
        R_n = math.sqrt((X**2)+(Y**2)+(Z**2))

        f_rad = math.acos(((R_n**2)+(R_s**2)-(R_t**2))/(2*R_n*R_s))
        f_grad = f_rad*(180/math.pi)



#     We=7.2292115E-5
# c   We=0.
#     f=1/298.257
#     h=0
#     Re=6378.140
#     Rp=(1-f)*(Re+h) 
#     e2=6.694385E-3
#     p=42.841382
#     q=42.697725         

#     Fd=0.0         
#     Lam=0.000096        

#     Rs=sqrt((Xs)**2+(Ys)**2+(Zs)**2)
#     VS=sqrt((VSx)**2+(VSy)**2+(VSz)**2)  
#     Gam=acos((Rs**2+R**2-Rt**2)/(2*Rs*R))

#     Q=acos((Xs*VSx+Ys*VSy+Zs*VSz)/Rs/VS)
#     C=Rs*VS*sin(Q)

#     C1=Ys*VSz-Zs*VSy
#     C2=Zs*VSx-Xs*VSz
#     C3=Xs*VSy-Ys*VSx

#     nn11=1/(C*Rs)*(C2*Zs-C3*Ys)
#     nn12=C1/C
#     nn13=Xs/Rs

#     nn21=1/(C*Rs)*(C3*Xs-C1*Zs)
#     nn22=C2/C
#     nn23=Ys/Rs

#     nn31=1/(C*Rs)*(C1*Ys-C2*Xs)
#     nn32=C3/C
#     nn33=Zs/Rs

#     Fif=acos(R*sin(Gam)/Rt)

#     N1=Rt*cos(Fif)*((-VSx-We*Ys)*nn11-(VSy-We*Xs)*nn21
#     *   -VSz*nn31)
#     N2=Rt*cos(Fif)*((-VSx-We*Ys)*nn12-(VSy-We*Xs)*nn22
#     *   -VSz*nn32)+0.000000001D00
#     N0=Rt*sin(Fif)*((-VSx-We*Ys)*nn13-(VSy-We*Xs)*nn23 -VSz*nn33)+ Lam*Fd*R/2+ Xs*VSx+Ys*VSy+Zs*VSz

#     Lamf=asin(-N0/(sqrt(N1**2+N2**2)))-atan(N1/N2)
# c   Fd=2./Lam/R*(cos(Lamf)*N1+sin(Lamf)*N2-N0)

        
#     Lamf=Lamf*180./3.1415
#     if(Lamf.Lt.0) Lamf=180+Lamf





        #print(R_n,f_grad,dt)
        
        if f_grad < 60:
#  #           print (R_n)
            track_shape.point(lon_s, lat_s)
            track_shape.record(i, dt, lon_s, lat_s, R_s, R_t, R_n, f_grad)
            # Не забываем про счётчики
        i += 1
            
        dt += delta
 #       print(dt)
    print (i)
    # Вне цикла нам осталось записать созданный шейп-файл на диск.
    # Т.к. мы знаем, что координаты положений ИСЗ были получены в WGS84
    # можно заодно создать файл .prj с нужным описанием

    try:
        # Создаем файл .prj с тем же именем, что и выходной .shp
        prj = open("%s.prj" % output_shapefile.replace(".shp", ""), "w")
        # Создаем переменную с описанием EPSG:4326 (WGS84)
        wgs84_wkt = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
        # Записываем её в файл .prj
        prj.write(wgs84_wkt)
        # И закрываем его
        prj.close()
        # Функцией save также сохраняем и сам шейп.
       
    except:
        # Вдруг нет прав на запись или вроде того...
        print("Unable to save shapefile prj")
        return

#Задаем начальное время
dt_start = datetime(2024, 1, 25, 0, 0, 0)

print(dt_start)
create_orbital_track_shapefile_for_day(tle_1, tle_2, dt_start, "space/bars_m.shp")
