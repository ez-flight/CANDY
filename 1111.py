import math

from pyorbital.orbital import Orbital
from sgp4.api import Satrec
from sgp4.earth_gravity import wgs84
from tletools import TLE

from KeplerOrbit import KeplerOrbit

tle_string = """
SUOMI NPP
1 37849U 11061A   23280.08921149  .00000269  00000-0  14837-3 0  9992
2 37849  98.7111 216.9310 0000832  62.3537 308.8007 14.19576889618819
"""
# Нас интересует текущий момент времени
#utc_time = datetime.utcnow()
u=398600.44158 #геоцентрическая гравитационная постоянная

tle_lines = tle_string.strip().splitlines()
tle = TLE.from_lines(*tle_lines)

s_name , tle_1, tle_2 = tle_string.strip().splitlines()
T=(24*3600)/tle.n
chislo=(T*T*u)/(4*tle.n*tle.n)
stepen=1/3
sma=math.pow(chislo,stepen)
#print (sma)
orbit = KeplerOrbit(sma, tle.ecc, tle.inc, tle.argp, tle.raan, tle.M)
print("Вычисляет и возвращает период обращения спутника в секундах")
print(orbit.get_T())

print("Вывод на экран прямоугольных координат")
orbit.dispXYZ(0)
print("Вывод на экран составляющих прямоугольных скоростей")
orbit.dispXYZ1(0)
print("пересчёт прямоугольных координат в кеплеровы элементы орбиты")
orbit.dispEphem()

x, y, z, x1, y1, z1 = orbit.ephem2xyz(0)

print('--------------------------------')
orbit.xyz2ephem(x, y, z, x1, y1, z1)
orbit.dispEphem()
orbit.dispXYZ(0)
orbit.dispXYZ1(0)

x, y, z, x1, y1, z1 = orbit.ephem2xyz(100)

print('--------------------------------')
orbit.xyz2ephem(x, y, z, x1, y1, z1)

orbit.dispEphem()
orbit.dispXYZ(0)
orbit.dispXYZ1(0)

from sgp4.api import Satrec

line=['0 ISS (ZARYA)',
'1 25544U 98067A   21356.62544795  .00006800  00000-0  13125-3 0  9998',
'2 25544  51.6428 130.9420 0004657 342.5227  11.5462 15.49048823317794']
sat = Satrec.twoline2rv(line[1],line[2])
print((sat.alta * sat.radiusearthkm), (sat.altp * sat.radiusearthkm))



        if ϒ >  3.13:
            print ("Внимание!")
            print (ϒ)
        dgh = R_s*math.sin(ϒ)
        kgf = (dgh/R_0)
        if  kgf > 0:
            if kgf < math.pi:
                #ugol = math.acos(kgf)
                ugol =1
                #print ("Внимание!")     
                #print (ugol*(180/math.pi))
            else:
                print(f"{kgf},  {ϒ*(180/math.pi)}")