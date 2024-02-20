import math
from datetime import date, datetime, timedelta

# Библиотека графиков
import matplotlib.pyplot as plt
import numpy as np
import shapefile
# Ключевой класс библиотеки pyorbital
from pyorbital.orbital import Orbital

from calc_cord import get_xyzv_from_latlon
from calc_F_L import calc_f_doplera, calc_lamda
from read_TBF import read_tle_base_file, read_tle_base_internet

#from sgp4.earth_gravity import wgs84



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


def create_orbital_track_shapefile_for_day(tle_1, tle_2, dt_start, dt_end, delta, track_shape,pos_gt, a):
 
    # Угловая скорость вращения земли
    We = 7.2292115E-5
    # Радиус земли
    Re = 6378.140
    # Длина волны
    Lam=0.000096
    # Координаты объекта в геодезической СК
    lat_t, lon_t, alt_t = pos_gt
    lat_t = 59.95  #55.75583
    lon_t = 30.316667 #37.6173
    alt_t = 12
    # Время начала расчетов
    dt = dt_start

    Wp_m = []
    Fd_m = []

    # Объявляем счётчики, i для идентификаторов, minutes для времени
    i = 0
    # Цикл расчета в заданном интервале времени
    while dt < dt_end:
        # Считаем положение спутника в инерциальной СК
        X_s, Y_s, Z_s, Vx_s, Vy_s, Vz_s = get_position(tle_1, tle_2, dt)
        Rs = X_s, Y_s, Z_s
        Vs = Vx_s, Vy_s, Vz_s

        # Считаем положение спутника в геодезической СК
        lon_s, lat_s, alt_s = get_lat_lon_sgp(tle_1, tle_2, dt)

        #Персчитываем положение объекта из геодезической в инерциальную СК  на текущее время с расчетом компонентов скорости точки на земле
        pos_it, v_t = get_xyzv_from_latlon(dt, lon_t, lat_t, alt_t)
        X_t, Y_t, Z_t = pos_it

        #Расчет ----
        R_s = math.sqrt((X_s**2)+(Y_s**2)+(Z_s**2))
        R_0 = math.sqrt(((X_s-X_t)**2)+((Y_s-Y_t)**2)+((Z_s-Z_t)**2))
        R_e = math.sqrt((X_t**2)+(Y_t**2)+(Z_t**2))
        V_s = math.sqrt((Vx_s**2)+(Vy_s**2)+(Vz_s**2))

        #Расчет двух углов
        #Верхний (Угол Визирования)
        y = math.acos(((R_0**2)+(R_s**2)-(R_e**2))/(2*R_0*R_s))
        y_grad = y * (180/math.pi)
        #Нижний (Угол места)
        ay = math.acos(((R_0*math.sin(y))/R_e))
        ay_grad = math.degrees(ay)
#        if R_0 < 960:
        if  y_grad > 24 and y_grad < 55 and R_0 < R_e:
#            print (f"{y_grad:.0f} {ay:.0f}")
            #Расчет угловой скорости вращения земли для подспутниковой точки
            Wp = 1674 * math.cos(math.radians(lat_s))
            Wp_m.append(Wp)
     #       Wp = We * math.cos(lat_t)* Re
           # Расчет угла a ведется в файле calc_F_L.py резкльтат в градусах
            Fd = calc_f_doplera(a, Lam, ay, Rs, Vs, R_0, R_s, R_e, V_s)
            Fd_m.append(Fd)
#        print (f"Частота доплера - {Fd:.0f}, скорость {Wp}")
 #       print (f"{Fd}")
  #          print (R_0)
            # Создаём в шейп-файле новый объект
            # Определеяем геометрию
            track_shape.point(lon_s, lat_s)
            # и атрибуты
            track_shape.record(i, dt, lon_s, lat_s, R_s, R_e, R_0, y_grad, ay_grad, a, Fd)
            # Не забываем про счётчики
 #       print(ugol)
        i += 1
        dt += delta

 #   print (i)
    return track_shape, Wp_m, Fd_m
   


def _test():

    #25544 37849
    # 56756 Кондор ФКА
    s_name, tle_1, tle_2 = read_tle_base_file(56756)
    #s_name, tle_1, tle_2 = read_tle_base_internet(37849)
        
    # Координаты объекта в геодезической СК

    lat_t = 59.95  #55.75583
    lon_t = 30.316667 #37.6173
    alt_t = 12
    pos_gt_1 = lat_t, lon_t, alt_t
    pos_gt_2 = [55.75583, 30.316667, 140]

    filename = "space/" + s_name + ".shp"
    print (filename)
    # Создаём экземпляр класса Writer для создания шейп-файла, указываем тип геометрии
    track_shape = shapefile.Writer(filename, shapefile.POINT)

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
    track_shape.field("ϒ", "F", 40, 5)
    track_shape.field("φ", "F", 40, 5)
    track_shape.field("λ", "F", 40, 5)
    track_shape.field("f", "F", 40, 5)

     
    #Задаем начальное время
    dt_start = datetime(2024, 2, 21, 3, 0, 0)
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

    #Задаем количество суток для прогноза
    dt_end = dt_start + timedelta(
        days=16,
#        seconds=5689,
        seconds=0,
        microseconds=0,
        milliseconds=0,
        minutes=0,
        hours=0,
        weeks=0
    )
    a = 90

#    while  a <= 92:
#        track_shape, acc, abb = create_orbital_track_shapefile_for_day(tle_1, tle_2, dt_start, dt_end, delta, track_shape,pos_gt, a)
#        ass1.append(acc)
#        Fd_m.append(abb)
#        a += 1
    track_shape, acc1, abb1 = create_orbital_track_shapefile_for_day(tle_1, tle_2, dt_start, dt_end, delta, track_shape,pos_gt_1, a)


    track_shape1, acc2, abb2 = create_orbital_track_shapefile_for_day(tle_1, tle_2, dt_start, dt_end, delta, track_shape,pos_gt_2, a)

    plt.title('Доплеровское смещение частоты отраженного сигнала в зависимости от угла скоса и угловой скорости подспутниковой точки')
    plt.xlabel('скорость подспутниковой точки')
    plt.ylabel('Fd,Гц')
    plt.plot(acc1, abb1, 'ro')
    plt.plot(acc2, abb2, 'bo')
#    plt.plot(ass1[4], Fd_m[4], 'yo')
    plt.show()

    # Вне цикла нам осталось записать созданный шейп-файл на диск.
    # Т.к. мы знаем, что координаты положений ИСЗ были получены в WGS84
    # можно заодно создать файл .prj с нужным описанием
           
       
    try:
        # Создаем файл .prj с тем же именем, что и выходной .shp
        prj = open("%s.prj" % filename.replace(".shp", ""), "w")
        # Создаем переменную с описанием EPSG:4326 (WGS84)
        wgs84_wkt = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
        # Записываем её в файл .prj
        prj.write(wgs84_wkt)
        # И закрываем его
        prj.close()
        # Функцией save также сохраняем и сам шейп.
        track_shape.save(filename)
    except:
        # Вдруг нет прав на запись или вроде того...
        print("Unable to save shapefile")
        return

if __name__ == "__main__":
    _test()