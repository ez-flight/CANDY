from datetime import datetime

from sgp4.earth_gravity import wgs84
from sgp4.io import twoline2rv

from read_TBF import read_tle_base_internet

current_time = datetime.utcnow()

# Пример TLE данных для спутника NOAA-19
s_name, tle_1, tle_2 = read_tle_base_internet(33591)

# Создаем объект TLE из данных
satellite = twoline2rv(tle_1, tle_2, wgs84)

# Вычисляем параметры орбиты, включая высоту
position, velocity = satellite.propagate(
    current_time.year, current_time.month, current_time.day,
    current_time.hour, current_time.minute, current_time.second
)
altitude = position[2]  # Высота над поверхностью Земли в километрах
print (velocity)
print(f"Высота спутника: {altitude} км")