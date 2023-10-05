import os
from dotenv import (
    load_dotenv,
)  # Импортируем библиотеки - для начала оговоренные ранее
from datetime import datetime, date, timedelta
import spacetrack.operators as op
from spacetrack import SpaceTrackClient
from pyorbital.orbital import Orbital

# И pyshp, которая понадобится для создания шейп-файла
import shapefile

load_dotenv()

# Имя пользователя и пароль сейчас опишем как константы
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


# Уже описанная ранее функция get_spacetrack_tle может использоваться без изменений
def get_spacetrack_tle(
    sat_id, start_date, end_date, username, password, latest=False
):
    st = SpaceTrackClient(identity=username, password=password)
    if not latest:
        daterange = op.inclusive_range(start_date, end_date)
        data = st.tle(
            norad_cat_id=sat_id,
            orderby="epoch desc",
            limit=1,
            format="tle",
            epoch=daterange,
        )
    else:
        data = st.tle_latest(
            norad_cat_id=sat_id, orderby="epoch desc", limit=1, format="tle"
        )

    if not data:
        return 0, 0

    tle_1 = data[0:69]
    tle_2 = data[70:139]
    return tle_1, tle_2


# А вот функция get_lat_lon_sgp нам уже не пригодится в своём виде
# ведь создавать экземпляр класса Orbital для каждого момента времени
# не очень-то хочется


# На вход будем требовать идентификатор спутника, день (в формате date (y,m,d))
# шаг в минутах для определения положения спутника, путь для результирующего файла
def create_orbital_track_shapefile_for_day(
    sat_id, track_day, step_minutes, output_shapefile
):
    # Для начала получаем TLE
    # Если запрошенная дата наступит в будущем, то запрашиваем самые последний набор TLE
    if track_day > date.today():
        tle_1, tle_2 = get_spacetrack_tle(
            sat_id, None, None, USERNAME, PASSWORD, True
        )
    # Иначе на конкретный период, формируя запрос для указанной даты и дня после неё
    else:
        tle_1, tle_2 = get_spacetrack_tle(
            sat_id,
            track_day,
            track_day + timedelta(days=1),
            USERNAME,
            PASSWORD,
            False,
        )

    # Если не получилось добыть
    if not tle_1 or not tle_2:
        print("Impossible to retrieve TLE")
        return

    # Создаём экземляр класса Orbital
    orb = Orbital("N", line1=tle_1, line2=tle_2)

    # Создаём экземпляр класса Writer для создания шейп-файла, указываем тип геометрии
    track_shape = shapefile.Writer(output_shapefile,shapefile.POINT)

    # Добавляем поля - идентификатор, время, широту и долготу
    # N - целочисленный тип, C - строка, F - вещественное число
    # Для времени придётся использовать строку, т.к. нет поддержки формата "дата и время"
    track_shape.field("ID", "N", 40)
    track_shape.field("TIME", "C", 40)
    track_shape.field("LAT", "F", 40)
    track_shape.field("LON", "F", 40)

    # Объявляем счётчики, i для идентификаторов, minutes для времени
    i = 0
    minutes = 0

    # Простой способ пройти сутки - с заданным в минутах шагом дойти до 1440 минут.
    # Именно столько их в сутках!
    while minutes < 1440:
        # Расчитаем час, минуту, секунду (для текущего шага)
        utc_hour = int(minutes // 60)
        utc_minutes = int((minutes - (utc_hour * 60)) // 1)
        utc_seconds = int(
            round((minutes - (utc_hour * 60) - utc_minutes) * 60)
        )

        # Сформируем строку для атрибута
        utc_string = (
            str(utc_hour) + "-" + str(utc_minutes) + "-" + str(utc_seconds)
        )
        # И переменную с временем текущего шага в формате datetime
        utc_time = datetime(
            track_day.year,
            track_day.month,
            track_day.day,
            utc_hour,
            utc_minutes,
            utc_seconds,
        )

        # Считаем положение спутника
        lon, lat, alt = orb.get_lonlatalt(utc_time)

        # Создаём в шейп-файле новый объект
        # Определеяем геометрию
        track_shape.point(lon, lat)
        # и атрибуты
        track_shape.record(i, utc_string, lat, lon)

        # Не забываем про счётчики
        i += 1
        minutes += step_minutes

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


create_orbital_track_shapefile_for_day(
    25994, date(2016, 12, 15), 5, "/home/ez/space/terra_15_12_2016_5min.shp"
)
