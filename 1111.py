import math
from datetime import date, datetime, timedelta

import shapefile

from calc_F_L import calc_f_doplera, calc_lamda
from candy import get_lat_lon_sgp, get_position, get_xyzv_from_latlon


def create_orbital_track_for_f_doplera(tle_1, tle_2, dt_start, pos_t, Lam_f):
     
    lon_t, lat_t, alt_t  = pos_t
#    Fd=0.0
    ugol = 90
    #Кондор, длина волны 10 см, частота   3200
    # Полоса рабочих частот, МГц 3100-3300
    F_zi = 3200 #МГц
    Lam= 0.299792458/F_zi #Получаем длину волны в метрах
#    print(f"{Lam:.6f}")

    dt = dt_start

    # Объявляем счётчики, i для идентификаторов, minutes для времени
    i = 0
 
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
    y = math.acos(((R_0**2)+(R_s**2)-(R_e**2))/(2*R_0*R_s))
    y_grad = y * (180/math.pi)
    ay = math.acos(((R_0*math.sin(y))/R_e))
    ay_grad = math.degrees(ay)
    Fd = calc_f_doplera (Lam_f, Lam, ay, Rs, Vs, R_0, R_s, R_e, V_s)

    return  dt, lon_s, lat_s, R_s, R_e, R_0, y_grad, ay_grad, Lam_f, Fd



def _test():

    tle_1 = '1 56756U 23074A   24029.75507617  .00007830  00000+0  37007-3 0  9997'
    tle_2 = '2 56756  97.4361 225.8387 0001732  73.7060 286.4365 15.19669782 37640'

     
    #Задаем начальное время
    dt_start = datetime(2024, 2, 21, 3, 0, 0)
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
        days=0,
        seconds=5689,
        microseconds=0,
        milliseconds=0,
        minutes=0,
        hours=0,
        weeks=0
    )
    
    filename = "space/proba.shp"
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


    #Координаты объекта в геодезической СК (lat,lon, alt)
    pos_t = 59.95, 30.316667, 12
 #   pos_t_2 = 61.796111, 34.349167, 112
    
    i = 0
 #   Lam_f = 88
    mas =  []
    mas_2 = []
    while dt_start < dt_end:
 #       print(dt_start)
        for Lam_f in range(88,93):
 #           print(Lam_f)
            mas.append(create_orbital_track_for_f_doplera(tle_1, tle_2, dt_start, pos_t, Lam_f))
 #           if Fd_1 > abs(Fd_2):
 #               Fd = Fd_2
 #               Lam_f_0 = Lam_f_2
 #           else:
 #               Fd = Fd_1
 #               Lam_f_0 = Lam_f_1
            Lam_f += 1
        mas.sort(key=lambda x:x[9])
        mas_2.append(mas[0])
        track_shape.point(mas[0][1], mas[0][2])
        track_shape.record(i, mas[0][0], mas[0][1], mas[0][2], mas[0][3], mas[0][4], mas[0][5], mas[0][6], mas[0][7], mas[1][8], mas[0][9])
        mas =  []
        
 #       mas_3.append(mas_2[0])
 #       mas = []
        i += 1
  #      print (i)
        dt_start += delta
    #sorted(maskey=lambda x: x[1])
#    print (mas_2)


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

