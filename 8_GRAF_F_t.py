import math
from datetime import date, datetime, timedelta

# Не забываем импортировать matplotlib.pyplot
import matplotlib.pyplot as plt
import numpy as np
import shapefile
import xlwt
# Ключевой класс библиотеки pyorbital
from pyorbital.orbital import Orbital

from calc_cord import get_xyzv_from_latlon
from calc_F_L import calc_f_doplera
from read_TBF import read_tle_base_file

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


def create_orbital_track_shapefile_for_day(tle_1, tle_2, pos_t, dt_start, dt_end, delta, track_shape, a, R_0):
 
    # Длина волны
    Lam=0.000096
    # Координаты объекта в геодезической СК
    lat_t, lon_t, alt_t = pos_t

    # Время начала расчетов
    dt = dt_start

    time_mass = []
    F_mass = []
    R_0_mass = []
    lat_mass = []
    lon_mass = []

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
        lon_mass.append(lon_s)
        lat_mass.append(lat_s)
        #Персчитываем положение объекта из геодезической в инерциальную СК  на текущее время с расчетом компонентов скорости точки на земле
        pos_t, v_t = get_xyzv_from_latlon(dt, lon_t, lat_t, alt_t)
        X_t, Y_t, Z_t = pos_t

        #Расчет ----
        R_s = math.sqrt((X_s**2)+(Y_s**2)+(Z_s**2))
#        R_0 = math.sqrt(((X_s-X_t)**2)+((Y_s-Y_t)**2)+((Z_s-Z_t)**2))
        R_e = math.sqrt((X_t**2)+(Y_t**2)+(Z_t**2))
        V_s = math.sqrt((Vx_s**2)+(Vy_s**2)+(Vz_s**2))

        #Расчет двух углов
        #Верхний (Угол Визирования)
        y = math.acos(((R_0**2)+(R_s**2)-(R_e**2))/(2*R_0*R_s))
        y_grad = y * (180/math.pi)
        #Нижний (Угол места)
        ay = math.acos(((R_0*math.sin(y))/R_e))
        ay_grad = math.degrees(ay)
# 
        date_delta = dt - dt_start
        time_mass.append(date_delta.total_seconds())

        R_0_mass.append(R_0)

        # Расчет угла a ведется в файле calc_F_L.py резкльтат в градусах
        Fd = calc_f_doplera(a, Lam, ay, Rs, Vs, R_0, R_s, R_e, V_s)
        F_mass.append(Fd)

        # Создаём в шейп-файле новый объект
        # Определеяем геометрию
        track_shape.point(lon_s, lat_s)
        # и атрибуты
        track_shape.record(i, dt, lon_s, lat_s, R_s, R_e, R_0, y_grad, ay_grad, a, Fd)
        # Не забываем про счётчики
 #      print(ugol)
        i += 1
        dt += delta
    Fd_min = min(F_mass)
    Fd_min = Fd_min/1000
    Fd_max = max(F_mass)
    Fd_max = Fd_max/1000
    return track_shape, time_mass, F_mass, R_0_mass, lat_mass, lon_mass, Fd_min, Fd_max
   
def create_buff_F_ot_R(tle_1, tle_2, pos_t, dt_start, dt_end, delta, track_shape, a, R0_min, R0_max):
    dist_mass = []
    Fd_max_mass = []
    Fd_min_mass = []
    for kk in range(R0_min, R0_max):
#                    ):
        track_shape, time_m, Fd_m, R_0_m, lat_m, lon_m, Fd_min, Fd_max = create_orbital_track_shapefile_for_day(tle_1, tle_2, pos_t, dt_start, dt_end, delta, track_shape, a, kk)
        dist_mass.append(kk)
        Fd_min_mass.append(Fd_min)
        Fd_max_mass.append(Fd_max)
    return dist_mass, Fd_min_mass, Fd_max_mass


def _test():

    book = xlwt.Workbook(encoding="utf-8")
    #25544 37849
    # 56756 Кондор ФКА
    s_name, tle_1, tle_2 = read_tle_base_file(56756)
    a = 88
    filename = "8_GRAF/8_GRAF_F_t" + s_name + ".shp"
    print (filename)

    lat_t = 59.95  #55.75583
    lon_t = 30.316667 #37.6173
    alt_t = 12
    pos_t = [lat_t, lon_t, alt_t]
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
    dt_start = datetime(2024, 2, 21, 19, 57, 00)
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
        days=0,
        seconds=5689,
#        seconds=0,
        microseconds=0,
        milliseconds=0,
        minutes=0,
        hours=0,
        weeks=0
    )

    dist_mass = []
    Fd_max_mass = []
    Fd_min_mass = []

    while  a <= 92:
        dist_m, Fd_min_m, Fd_max_m = create_buff_F_ot_R(tle_1, tle_2, pos_t, dt_start, dt_end, delta, track_shape, a, R0_min = 561, R0_max = 964)
        print(len(dist_m))
        dist_mass.append(dist_m)
        Fd_min_mass.append(Fd_min_m)
        Fd_max_mass.append(Fd_max_m)
        print(a)
        a += 2

    for ii in range(len(Fd_min_mass)):
        sheet1 = book.add_sheet(str(ii))
        for num in range(len(dist_m)):
            row = sheet1.row(num)
            row.write(0, dist_mass [ii] [num])
            row.write(1, Fd_min_mass [ii] [num])
            row.write(2, Fd_max_mass [ii] [num])

    # Save the result
    book.save("8_GRAF/8_GRAF_F_R_0" + s_name + ".xls") 

    # Создали объекты окна fig
    fig, (gr_1, gr_2) = plt.subplots(nrows=2)
    # Задали расположение графиков в 2 строки
    gr_1.plot(dist_mass[0], Fd_max_mass[0], 'r', linestyle='--', label="Угол $α$ = -2")
    gr_1.plot(dist_mass[1], Fd_max_mass[1], 'g', label="Угол $α$ = 0")
    gr_1.plot(dist_mass[2], Fd_max_mass[2], 'b', linestyle='dotted', label="Угол $α$ = +2")
    gr_2.plot(dist_mass[0], Fd_min_mass[0], 'r', linestyle='--', label="Угол $α$ = -2")
    gr_2.plot(dist_mass[1], Fd_min_mass[1], 'g', label="Угол $α$ = 0")
    gr_2.plot(dist_mass[2], Fd_min_mass[2], 'b', linestyle='dotted', label="Угол $α$ = +2")
   # Подписываем оси, пишем заголовок
#    gr_1.set_title('Доплеровское смещение частоты отраженного сигнала в зависимости от наклонной дальности')
    gr_1.set_ylabel('Fd, КГц')
    gr_2.set_ylabel('Fd, КГц')
    gr_2.set_xlabel('Наклонная дальность, км')
    gr_1.legend()
    # Отображаем сетку
    gr_1.grid(True)
    gr_2.grid(True)
    plt.show()


if __name__ == "__main__":
    _test()
