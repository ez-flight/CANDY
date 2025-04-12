import math
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import shapefile
import xlwt
from pyorbital import tlefile
from pyorbital.orbital import Orbital

from calc_cord import get_xyzv_from_latlon
from calc_F_L import calc_f_doplera, calc_lamda
from read_TBF import read_tle_base_file


def get_lat_lon_sgp(tle_1, tle_2, utc_time):
    """Получение географических координат спутника."""
    orb = Orbital("N", line1=tle_1, line2=tle_2)
    lon, lat, alt = orb.get_lonlatalt(utc_time)
    return lon, lat, alt

def get_position(tle_1, tle_2, utc_time):
    """Получение позиции и скорости спутника в инерциальной СК."""
    orb = Orbital("N", line1=tle_1, line2=tle_2)
    R_s, V_s = orb.get_position(utc_time, False)
    return R_s, V_s

def create_orbital_track_shapefile_for_day(tle_1, tle_2, pos_t, dt_start, dt_end, delta, track_shape, a):
    We = 7.2292115E-5  # Угловая скорость Земли, рад/с
    Re = 6378.140      # Экваториальный радиус Земли, км
    Lam = 0.0001       # Длина волны, км (0.1 м)
    lat_t, lon_t, alt_t = pos_t
    dt = dt_start

    time_mass, F_mass, R_0_mass, lat_mass, lon_mass = [], [], [], [], []

    while dt < dt_end:
        try:
            R_s_vec, V_s_vec = get_position(tle_1, tle_2, dt)
            X_s, Y_s, Z_s = R_s_vec
            Vx_s, Vy_s, Vz_s = V_s_vec

            lon_s, lat_s, _ = get_lat_lon_sgp(tle_1, tle_2, dt)
            pos_t, v_t = get_xyzv_from_latlon(dt, lon_t, lat_t, alt_t)
            X_t, Y_t, Z_t = pos_t

            R_s = math.sqrt(X_s**2 + Y_s**2 + Z_s**2)  # Норма вектора положения спутника
            R_0 = 750
#            R_0 = math.sqrt((X_s - X_t)**2 + (Y_s - Y_t)**2 + (Z_s - Z_t)**2)  # Расстояние до объекта
            R_e = math.sqrt(X_t**2 + Y_t**2 + Z_t**2)  # Радиус Земли в точке объекта
            V_s_norm = math.sqrt(Vx_s**2 + Vy_s**2 + Vz_s**2)  # Скорость спутника

            # Угол визирования и угол места
            y = math.acos((R_0**2 + R_s**2 - R_e**2) / (2 * R_0 * R_s))
            ay = math.acos((R_0 * math.sin(y)) / R_e)

            Fd = calc_f_doplera(a, Lam, ay, (X_s, Y_s, Z_s), (Vx_s, Vy_s, Vz_s), 
                                R_0, R_s, R_e, V_s_norm) / 1000  # Частота в кГц

            time_mass.append((dt - dt_start).total_seconds())
            F_mass.append(Fd)
            R_0_mass.append(R_0)
            lat_mass.append(lat_s)
            lon_mass.append(lon_s)

            # Запись данных в shapefile
            track_shape.point(lon_s, lat_s)
            track_shape.record(
                len(time_mass), 
                dt.strftime("%Y-%m-%d %H:%M:%S"), 
                round(lon_s, 5), 
                round(lat_s, 5), 
                round(R_s, 2), 
                round(R_e, 2), 
                round(R_0, 2), 
                round(math.degrees(y), 2), 
                round(math.degrees(ay), 2), 
                a, 
                round(Fd, 4)
            )
        except Exception as e:
            print(f"Ошибка на {dt}: {e}")
        dt += delta

    return track_shape, time_mass, F_mass, R_0_mass, lat_mass, lon_mass

def _test():
    # Пример использования
    norad_id = 56756  # Пример для спутника "Кондор"
    s_name, tle_1, tle_2 = read_tle_base_file(norad_id)
    a_values = [88, 90, 92]
    
    # Настройки времени
    dt_start = datetime(2024, 2, 21, 19, 57)
    delta = timedelta(seconds=10)
    dt_end = dt_start + timedelta(seconds=5689)

    # Подготовка графиков
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    for a in a_values:
        try:
            # Создание шейп-файла
            track_shape = shapefile.Writer(f"track_a{a}.shp", shapefile.POINT)
            track_shape.field("ID", "N", 40)
            track_shape.field("TIME", "C", 40)
            track_shape.field("LON", "F", 40, 5)
            track_shape.field("LAT", "F", 40, 5)
            track_shape.field("R_s", "F", 40, 2)
            track_shape.field("R_t", "F", 40, 2)
            track_shape.field("R_n", "F", 40, 2)
            track_shape.field("ϒ", "F", 40, 2)
            track_shape.field("φ", "F", 40, 2)
            track_shape.field("λ", "F", 40, 2)
            track_shape.field("f", "F", 40, 4)

            # Расчет данных
            _, time_m, Fd_m, _, lat_m, _ = create_orbital_track_shapefile_for_day(
                tle_1, tle_2, [59.95, 30.316667, 12], dt_start, dt_end, delta, track_shape, a)

            # Построение графиков
            ax1.plot(lat_m, Fd_m, label=f"α={a}°")
            ax2.plot(lat_m, time_m, label=f"α={a}°")

            # Сохранение шейп-файла
            track_shape.close()
        except Exception as e:
            print(f"Ошибка для a={a}: {e}")

    # Настройка графиков
    ax1.set_title('Доплеровская частота от широты')
    ax1.set_ylabel('Частота (кГц)')
    ax1.legend()
    ax1.grid(True)

    ax2.set_title('Время от широты')
    ax2.set_ylabel('Время (сек)')
    ax2.set_xlabel('Широта (°)')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig('doppler_analysis.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    _test()