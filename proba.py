import os
# Импортируем библиотеки
# Штатная библиотека для работы со временем
from datetime import date, datetime

from datetime import date, datetime, timedelta

# Собственно клиент для space-track
# Набор операторов для управления запросами. Отсюда нам понадобится время
import spacetrack.operators as op
from dotenv import load_dotenv
# Главный класс для работы с space-track
from spacetrack import SpaceTrackClient

load_dotenv()

# Имя пользователя и пароль сейчас опишем как константы
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


# Для примера реализуем всё в виде одной простой функции
# На вход она потребует идентификатор спутника, диапазон дат, имя пользователя и пароль. Опциональный флаг для последних данных tle
def get_spacetrack_tle(
    sat_id, start_date, end_date, username, password, latest=False
):
    # Реализуем экземпляр класса SpaceTrackClient, инициализируя его именем пользователя и паролем
    st = SpaceTrackClient(identity=username, password=password)
    # Выполнение запроса для диапазона дат:
    if not latest:
        # Определяем диапазон дат через оператор библиотеки
        daterange = op.inclusive_range(start_date, end_date)
        # Собственно выполняем запрос через st.tle
        data = st.tle(
            norad_cat_id=sat_id,
            orderby="epoch desc",
            limit=1,
            format="tle",
            epoch=daterange,
        )
    # Выполнение запроса для актуального состояния
    else:
        # Выполняем запрос через st.tle_latest
        data = st.tle_latest(
            norad_cat_id=sat_id, orderby="epoch desc", limit=1, format="tle"
        )

    # Если данные недоступны
    if not data:
        return 0, 0

    # Иначе возвращаем две строки
    tle_1 = data[0:69]
    tle_2 = data[70:139]
    return tle_1, tle_2


tle_1, tle_2 = get_spacetrack_tle(37849, None, None, USERNAME, PASSWORD, True)
print(tle_1)
print(tle_2)
