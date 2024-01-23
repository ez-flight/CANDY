# Импорт модуля math
import math
from datetime import date, datetime, timedelta
from cal_cord_2 import GSKtoISK
import shapefile

# Ключевой класс библиотеки pyorbital
from pyorbital.orbital import Orbital
from sgp4.api import Satrec
from sgp4.earth_gravity import wgs84

from cal_cord import geodetic_to_geocentric, fromLatLong
from read_TBF import read_tle_base_file, read_tle_base_internet

#25544 37849
#s_name, tle_1, tle_2 = read_tle_base_file(37849)
s_name, tle_1, tle_2 = read_tle_base_internet(37849)
utc_time = datetime.utcnow()
sat = Satrec.twoline2rv(tle_1,tle_2)

wgs_84 = (6378137., 1./298.257223563)

dt_start = datetime.now() + timedelta(
        days=0,
        seconds=0,
        microseconds=0,
        milliseconds=0,
        minutes=0,
        hours=0,
        weeks=0
    ) #Задаем шаг определения координат


R_z=wgs84.radiusearthkm # радиус земли
#R_z= 6378.137
#H_a=505#sat.alta * R_z # высота апогея
#H_p=sat.altp * R_z # высота перегея

u=398600.44158 #геоцентрическая гравитационная постоянная

# Ещё одна простая функция, для демонстрации принципа.
# На вход она потребует две строки tle и время utc в формате datetime.datetime
def get_lat_lon_sgp (tle_1, tle_2, utc_time):
    # Инициализируем экземпляр класса Orbital двумя строками TLE
    orb = Orbital("N", line1=tle_1, line2=tle_2)
    # Вычисляем географические координаты функцией get_lonlatalt, её аргумент - время в UTC.
    lon, lat, alt = orb.get_lonlatalt(utc_time)
    return lon, lat, alt

def get_position (tle_1, tle_2, utc_time):
    # Инициализируем экземпляр класса Orbital двумя строками TLE
    orb = Orbital("N", line1=tle_1, line2=tle_2)
    # Вычисляем географические координаты функцией get_lonlatalt, её аргумент - время в UTC.
    R_s, V_s = orb.get_position(utc_time,False)
    X_s, Y_s, Z_s = R_s
    Vx_s, Vy_s, Vz_s = V_s
    return X_s, Y_s, Z_s, Vx_s, Vy_s, Vz_s



#X_t, Y_t, Z_t = geodetic_to_geocentric(lat, lon, h, af)

# Обращаемся к фукнции и выводим результат
#lon, lat, alt = get_lat_lon_sgp (tle_1, tle_2, utc_time)
#X_s, Y_s, Z_s, Vx_s, Vy_s, Vz_s =get_position (tle_1, tle_2, utc_time)

#R_n = math.sqrt(((X_s-X_t)**2)+((Y_s-Y_t)**2)+((Z_s-Z_t)**2))

#res1 = math.sqrt((X_s**2)+(Y_s**2)+(Z_s**2))
#res2 = math.sqrt((Vx_s**2)+(Vy_s**2)+(Vz_s**2))

def create_orbital_track_shapefile_for_day(tle_1, tle_2, dt_start, step_minutes, output_shapefile):

    lat_t = 59.95
    lon_t = 30.316667
    h_t = 12
    delta = timedelta(
        days=0,
        seconds=0,
        microseconds=0,
        milliseconds=0,
        minutes=step_minutes,
        hours=0,
        weeks=0
    ) #Задаем шаг определения координат

    dt_end = dt_start + timedelta(
        days=3,
        seconds=0,
        microseconds=0,
        milliseconds=0,
        minutes=0,
        hours=0,
        weeks=0
    )
    dt = dt_start


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
    minutes = 0

    # Простой способ пройти сутки - с заданным в минутах шагом дойти до 1440 минут.
    # Именно столько их в сутках!
    while dt<dt_end:
        # Расчет инерциальных пара
        X_s, Y_s, Z_s, Vx_s, Vy_s, Vz_s = get_position (tle_1, tle_2, dt)
        X_gsk, Y_gsk, Z_gsk = fromLatLong(lat_t, lon_t, h_t, wgs_84)
        X_t, Y_t, Z_t = GSKtoISK(dt, X_gsk, Y_gsk, Z_gsk)
        R_s = math.sqrt((X_s**2)+(Y_s**2)+(Z_s**2))
        X = (X_s-X_t)
        Y = (Y_s-Y_t)
        Z = (Z_s-Z_t)
        R_n = math.sqrt((X**2)+(Y**2)+(Z**2))
        R_t = math.sqrt((X_t**2)+(Y_t**2)+(Z_t**2))
        f_rad = math.acos(((R_n**2)+(R_s**2)-(R_t**2))/(2*R_n*R_s))
        f_grad = f_rad*(180/3.14)
        # Считаем положение спутника
        lon, lat, alt = get_lat_lon_sgp (tle_1, tle_2, dt)
#        print(f"Наклонная Дальность -> {R_n:2f}  Ф -> {f_grad} в {dt}")
        if R_n < 1000:
            # Создаём в шейп-файле новый объект
            # Определеяем геометрию
            track_shape.point(lon, lat)
            # и атрибуты
            track_shape.record(i, dt, lon, lat, R_s, R_t, R_n, f_grad)
            # Не забываем про счётчики
            i += 1
            
        dt += delta
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
    
create_orbital_track_shapefile_for_day(tle_1,tle_2, dt_start, 2, "/home/ez/space/Suomi NPP/Suomi_NPP_5min.shp")