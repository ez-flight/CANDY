# Импорт модуля math
import math
from datetime import date, datetime, timedelta

import numpy as np
import shapefile
# Ключевой класс библиотеки pyorbital
from pyorbital.orbital import Orbital
from sgp4.api import Satrec
from sgp4.earth_gravity import wgs84

from cal_cord import (geodetic_to_geocentric, geodetic_to_ISK,
                      get_xyzv_from_latlon)
from read_TBF import read_tle_base_file, read_tle_base_internet

#25544 37849
# 56756 Кондор ФКА
s_name, tle_1, tle_2 = read_tle_base_file(56756)
#s_name, tle_1, tle_2 = read_tle_base_internet(37849)

filename = "space/" + s_name + ".shp"
print (filename)
sat = Satrec.twoline2rv(tle_1, tle_2)

wgs_84 = (6378137, 298.257223563)

R_z=wgs84.radiusearthkm # радиус земли
#R_z= 6378.137
u=398600.44158 #геоцентрическая гравитационная постоянная


def get_lat_lon_sgp(tle_1, tle_2, utc_time):
    # Инициализируем экземпляр класса Orbital двумя строками TLE
    orb = Orbital("N", line1=tle_1, line2=tle_2)
    # Вычисляем географические координаты функцией get_lonlatalt, её аргумент - время в UTC.
    lon, lat, alt = orb.get_lonlatalt(utc_time)
    return lon, lat, alt


def get_position(tle_1, tle_2, utc_time):
    # Инициализируем экземпляр класса Orbital двумя строками TLE
    orb = Orbital("N", line1=tle_1, line2=tle_2)
    # Вычисляем географические координаты функцией get_lonlatalt, её аргумент - время в UTC.
    R_s, V_s = orb.get_position(utc_time, False)
    X_s, Y_s, Z_s = R_s
    Vx_s, Vy_s, Vz_s = V_s
    return X_s, Y_s, Z_s, Vx_s, Vy_s, Vz_s


def create_orbital_track_shapefile_for_day(tle_1, tle_2, dt_start, output_shapefile):

    We=7.2292115E-5
 #   We=0.

 #   Re=6378.140
 
    e2=6.694385E-3
    p=42.841382
    q=42.697725

    #Кондор, длина волны 10 см, частота   3200
    # Полоса рабочих частот, МГц 3100-3300
    Fd=0.0
    F_zi = 3200000000
    L_ps= 0.299792458/F_zi
 #   print(L_ps)
#    print (0.299792458/0.000096)
    #Координаты объекта в геодезической СК
    lat_t = 59.95  #55.75583
    lon_t = 30.316667 #37.6173
    alt_t = 12

    #Задаем шаг по времени для прогноза
    delta = timedelta(
        days=0,
        seconds=30,
        microseconds=0,
        milliseconds=0,
        minutes=0,
        hours=0,
        weeks=0
    )

    #Задаем количество суток для прогноза
    dt_end = dt_start + timedelta(
        days=30,
        seconds=0,
        microseconds=0,
        milliseconds=0,
        minutes=0,
        hours=0,
        weeks=0
    )
    dt = dt_start

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
    track_shape.field("ϒ", "F", 40)
    track_shape.field("φ", "F", 40)
#    track_shape.field("Lamf", "F", 40)
    track_shape.field("Fd", "F", 40)
    # Объявляем счётчики, i для идентификаторов, minutes для времени
    i = 0

    while dt < dt_end:
        # Считаем положение спутника в инерциальной СК
        X_s, Y_s, Z_s, Vx_s, Vy_s, Vz_s = get_position (tle_1, tle_2, dt)

        # Считаем положение спутника в геодезической СК
        lon_s, lat_s, alt_s = get_lat_lon_sgp(tle_1, tle_2, dt)

        #Персчитываем положение объекта из геодезической в инерциальную СК  на текущее время с расчетом компонентов скорости точки на земле
        pos_t, v_t = get_xyzv_from_latlon(dt, lon_t, lat_t, alt_t)
        X_t, Y_t, Z_t = pos_t

        #Расчет ----
        R_s = math.sqrt((X_s**2)+(Y_s**2)+(Z_s**2))
        R_0 = math.sqrt(((X_s-X_t)**2)+((Y_s-Y_t)**2)+((Z_s-Z_t)**2))
        R_e = math.sqrt((X_t**2)+(Y_t**2)+(Z_t**2))
        V_s = math.sqrt((Vx_s**2)+(Vx_s**2)+(Vx_s**2))

        #Расчеты Для формул ??????
        f=1/298.257
        h=0
        Rp=(1-f)*(R_e + h)

        y = math.acos(((R_0**2)+(R_s**2)-(R_e**2))/(2*R_0*R_s))
        y_grad = y * (180/math.pi)
        #Постоянная площадей
        Q = math.acos(((X_s*Vx_s)+(Y_s*Vy_s)+(Z_s*Vz_s))/(R_s/V_s))
        C = R_s*V_s*math.sin(Q)
        #Расчет компонентов вектора площадей
        C1 = Y_s*Vz_s-Z_s*Vy_s
        C2 = Z_s*Vx_s-X_s*Vz_s
        C3 = X_s*Vy_s-Y_s*Vx_s
        #Расчет матрицы поворота
        nn11 = 1/(C*R_s)*(C2*Z_s-C3*Y_s)
        nn12 = C1/C
        nn13 = X_s/R_s

        nn21 = 1/(C*R_s)*(C3*X_s-C1*Z_s)
        nn22 = C2/C
        nn23 = Y_s/R_s

        nn31 = 1/(C*R_s)*(C1*Y_s-C2*X_s)
        nn32 = C3/C
        nn33 = Z_s/R_s

        fi = math.acos(R_s*math.sin(y)/R_e) 
        fi_grad = fi * (180/math.pi)
        #Определение вектора наклонной дальности
        N1 = R_e*math.cos(fi)*(((-Vx_s-(We*Y_s))*nn11-(Vy_s-(We*X_s))*nn21) - (Vz_s * nn31))
        N2 = R_e*math.cos(fi)*((-Vx_s-(We*Y_s))*nn12-(Vy_s-(We*X_s))*nn22 - (Vz_s * nn32))+0.000000001
        N0 = R_e*math.sin(fi)*((-Vx_s-(We*Y_s))*nn13-(Vy_s-(We*X_s))*nn23 -(Vz_s * nn33)) + (L_ps * Fd * R_0)/2 + (X_s * Vx_s) + (Y_s * Vy_s) + (Z_s * Vz_s)

        #Расчет угла при заданной Fd
        ugol = math.asin(-N0/(math.sqrt(N1**2 + N2**2)))-math.atan(N1/N2)
        ugol =ugol  * (180/math.pi)
        if(ugol < 0):
            ugol=180+ugol
       #Доплеровская частота отраженного сигнала
 #       Fd = 2./(L_ps*R_0*(math.cos(y)*N1+math.sin(y)*N2-N0))
        # Считаем положение спутника
 #       print(f"Наклонная Дальность -> {R_n:2f}  Ф -> {ϒ} в {dt}")
        
   #     if abs(Fd) < 20000:
  #          print (R_0)
            # Создаём в шейп-файле новый объект
            # Определеяем геометрию
        track_shape.point(lon_s, lat_s)
            # и атрибуты
        track_shape.record(i, dt, lon_s, lat_s, R_s, R_e, R_0, y_grad, fi_grad, ugol)
            # Не забываем про счётчики
        print(ugol)
        i += 1
        dt += delta

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
        track_shape.save(output_shapefile)
    except:
        # Вдруг нет прав на запись или вроде того...
        print("Unable to save shapefile")
        return
    
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

#Задаем начальное время
dt_start = datetime(2024, 2, 21, 0, 0, 0)

create_orbital_track_shapefile_for_day(tle_1, tle_2, dt_start, filename)
