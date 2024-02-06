import math
from datetime import date, datetime, timedelta
from calc_F_L import calc_f_doplera, calc_lamda
from candy import get_position, get_lat_lon_sgp, get_xyzv_from_latlon


def create_orbital_track_for_f_doplera(tle_1, tle_2, dt_start, dt_end, delta, pos_t, Lam_f):
     
    lon_t, lat_t, alt_t  = pos_t
#    Fd=0.0
    ugol = 90
    #Кондор, длина волны 10 см, частота   3200
    # Полоса рабочих частот, МГц 3100-3300
    F_zi = 3200 #МГц
    Lam= 0.299792458/F_zi #Получаем длину волны в метрах
    print(f"{Lam:.6f}")

    dt = dt_start

    # Объявляем счётчики, i для идентификаторов, minutes для времени
    i = 0

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
        y = math.acos(((R_0**2)+(R_s**2)-(R_e**2))/(2*R_0*R_s))
        y_grad = y * (180/math.pi)
        ay = math.acos(((R_0*math.sin(y))/R_e))
        ay_grad = math.degrees(ay)
 
        Fd = calc_f_doplera (Lam_f, Lam, ay, Rs, Vs, R_0, R_s, R_e, V_s)
        mas = i, dt, lon_s, lat_s, R_s, R_e, R_0, y_grad, ay_grad, Lam_f, Fd
        #print (f"{Fd:.5f}")
        i += 1
        dt += delta
        print (mas)



def _test():

    tle_1 = '1 25544U 98067A   23279.68733398  .00019024  00000+0  34211-3 0  9999'
    tle_2 = '2 25544  51.6400 136.2543 0005380  78.9726  28.2342 15.49856251419086'

     
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

    #Координаты объекта в геодезической СК (lat,lon, alt)
    pos_t = 59.95, 30.316667, 12

    create_orbital_track_for_f_doplera (tle_1, tle_2, dt_start, dt_end, delta, pos_t, Lam_f=90)


if __name__ == "__main__":
    _test()

