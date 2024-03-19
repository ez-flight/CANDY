# Библиотека графиков
import matplotlib.pyplot as plt
import numpy as np
# Import `xlrd`
import xlrd
import math
from datetime import date, datetime, timedelta

# Не забываем импортировать matplotlib.pyplot
import matplotlib.pyplot as plt
import numpy as np
import shapefile
# Ключевой класс библиотеки pyorbital
from pyorbital.orbital import Orbital

from calc_cord import get_xyzv_from_latlon
from calc_F_L import calc_f_doplera
from read_TBF import read_tle_base_file


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


def create_orbital_track_shapefile_for_day(tle_1, tle_2, pos_t, dt_start, dt_end, delta, track_shape, a):
 
    # Угловая скорость вращения земли
    We = 7.2292115E-5
    # Радиус земли
    Re = 6378.140
    # Длина волны
    Lam=0.000096
    # Координаты объекта в геодезической СК
    lat_t, lon_t, alt_t = pos_t

    # Время начала расчетов
    dt = dt_start

    time_mass = []
    F_mass = []
    R_0_mass = []

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
        pos_t, v_t = get_xyzv_from_latlon(dt, lon_t, lat_t, alt_t)
        X_t, Y_t, Z_t = pos_t

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

 #   print (i)
    return track_shape, time_mass, F_mass, R_0_mass
   


def _test():

filename = "t_max_semki"

# Open a workbook 
workbook = xlrd.open_workbook(filename + ".xls")
# Loads only current sheets to memory
workbook = xlrd.open_workbook(filename + ".xls", on_demand = True)
# Получаем количество листов в файле 
len_list = len(workbook.sheet_names())
for k in range(len_list):
    # Получить объект листа по индексу
    sheet1 = workbook.sheet_by_index(k)
    # Загрузите определенный лист по названию
    worksheet = workbook.sheet_by_name(sheet1.name)

    vitok = []
    dt_start = []
    dt_end = []
    t_simki= []

    for i in range(0, 27):
        for j in range(0, 3):
            if j == 0:
                vitok.append(worksheet.cell_value(i, j))
            elif j == 1:
                dt_start.append(worksheet.cell_value(i, j))
            elif j == 2:
                dt_end.append(worksheet.cell_value(i, j))
            elif j == 3:
                t_simki.append(worksheet.cell_value(i, j))

    s_name, tle_1, tle_2 = read_tle_base_file(56756)

    filename = "9_GRAF/9_GRAF_F_t" + s_name + ".shp"
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
    dt_start = datetime(2024, 2, 25, 3, 58, 8)
    #Задаем конечное время
 #   dt_end = datetime(2024, 3, 6, 17, 3, 17)
    #Задаем шаг по времени для прогноза
    delta = timedelta(
        days=0,
        seconds=1,
        microseconds=0,
        milliseconds=0,
        minutes=0,
        hours=0,
        weeks=0
    )

    #Задаем количество суток для прогноза
    dt_end = dt_start + timedelta(
        days=0,
        seconds=199,
#        seconds=0,
        microseconds=0,
        milliseconds=0,
        minutes=0,
        hours=0,
        weeks=0
    )

    time_mass = []
    Fd_mass = []
    R_0_mass = []
    
    while  a <= 92:
        track_shape, time_m, Fd_m, R_0_m = create_orbital_track_shapefile_for_day(tle_1, tle_2, pos_t, dt_start, dt_end, delta, track_shape, a)
        time_mass.append(time_m)
        Fd_mass.append(Fd_m)
        R_0_mass.append(R_0_m)
        a += 2
    # Создали объекты окна fig
    fig, (gr_1, gr_2) = plt.subplots(nrows=2)
    # Задали расположение графиков в 2 строки
    gr_1.plot(time_mass[0], Fd_mass[0], 'r', label="Угол $λ$ = 88")
    gr_1.plot(time_mass[1], Fd_mass[1], 'b', label="Угол $λ$ = 90")
    gr_1.plot(time_mass[2], Fd_mass[2], 'y', label="Угол $λ$ = 92")
    gr_2.plot(time_mass[0], R_0_mass[0], 'g', label="Угол $λ$ = 88")
    # Подписываем оси, пишем заголовок
#    gr_1.set_title('Доплеровское смещение частоты отраженного сигнала в зависимости времени')
    gr_1.set_ylabel('Fd (Гц)')
    gr_2.set_ylabel('R0 (м)')
    gr_2.set_xlabel('Время (сек)')
    gr_1.legend()
    # Отображаем сетку
    gr_1.grid(True)
    gr_2.grid(True)
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

