import math

# Задайте параметры вашей радиолокационной системы
orbit_height = 500 # высота орбиты спутника над землей в километрах
frequency_band = 5.6e9 # диапазон частот в герцах
azimuth_resolution = 5 # разрешение по азимуту в градусах
elevation_resolution = 0.5 # разрешение по углу места в градусах
satellite_speed = 7.5 # скорость спутника в километрах в секунду

# Вычисление времени распространения сигнала от цели до спутника
earth_radius = 6371 # радиус Земли в километрах
target_distance = orbit_height + earth_radius
signal_travel_time = target_distance / satellite_speed

# Вычисление времени интеграции для формирования изображения
azimuth_beamwidth = math.radians(azimuth_resolution)
elevation_beamwidth = math.radians(elevation_resolution)
integration_time = azimuth_beamwidth * elevation_beamwidth / (4 * math.pi * frequency_band)

# Вычисление общей длительности съемки
total_duration = signal_travel_time + integration_time

print(f"Длительность съемки: {total_duration} секунд")

# Дополнительные расчеты и вывод результатов
# ...