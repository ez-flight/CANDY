#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import math
from math import *


# попытка сделать класс для кеплеровых элементов орбит
#
#
#  такие функции:
#  def  ephem2xyz(self, dt):
#  def  xyz2ephem(self, x, y, z, x1, y1, z1):
#  def  dispXYZ(self, dT):
#  def  dispXYZ1(self, dT):
#  def  dispEphem(self):
#  def  __init__(self, a = 0, e = 0, i = 0, d = 0, w = 0, m_0 = 0):


MU = 398600.44150

class KeplerOrbit:

    def __init__(self, a = 0, e = 0, i = 0, d = 0, w = 0, m_0 = 0):
        ''' Инициализация
        '''
        # print('KeplerOrbit: инициализация')
        self.semimajor_axis   = a #большая полуось
        self.eccentricity     = e #эксцентриситет орбиты
        self.inclination  = i #наклонение
        self.draco     = d #аргумент перицентра
        self.omega     = w #долгота восходящего узла
        self.M_0       = m_0  #средняя аномалия
 
   
    def dispEphem(self):
        ''' Вывод на экран эфемерид
        '''
        print("a = {0:.2f}  e = {1:.3f}  i = {2:.3f}  d = {3:.3f}  w = {4:.3f}  M_0 = {5:.3f}".format(self.semimajor_axis, self.eccentricity, self.inclination, self.draco, self.omega, self.M_0))


    def dispXYZ(self, dT):
        ''' Вывод на экран прямоугольных координат
        '''
        x, y, z, x1, y1, z1 = self.ephem2xyz(dT)
        print("X = {0:9.3f} Y = {1:9.3f}  Z = {2:9.3f}".format(x, y, z))


    def dispXYZ1(self, dT):
        ''' Вывод на экран составляющих прямоугольных скоростей
        '''
        x, y, z, x1, y1, z1 = self.ephem2xyz(dT)
        print("X1= {0:9.3f} Y1= {1:9.3f}  Z1= {2:9.3f}".format(x1, y1, z1))


    def xyz2ephem(self, x, y, z, x1, y1, z1):
        ''' пересчёт прямоугольных координат в кеплеровы элементы орбиты
        '''

        #####       1       #####
        # вычисляем постоянные площадей
        c1 = y*z1 - y1*z
        c2 = x1*z - x*z1
        c3 = x*y1 - x1*y

        c = sqrt(c1**2 + c2**2 + c3**2)

        #####       2       #####
        # фокальный параметр
        p = c**2 / MU

        #####       3       #####
        # угол наклона орбиты к плоскости экватора
        if  c == 0:
            if c3 > 0:
                i = 0
            else:
                i = pi
        else:
            i = acos(c3 / c)

        #####       4       #####
        # долгота восходящего узла
        sin_Draco = c1 / (c*sin(i))

        cos_Draco = -c2 / (c*sin(i))

        if  sin_Draco >= 0:
            Draco = acos(cos_Draco)
        elif sin_Draco <= 0:
            Draco = 2*pi - acos(cos_Draco)
        else:
            cos_Draco = 1
            sin_Draco = 0
            Draco = 0
            print(cos_Draco)
            print(sin_Draco)
            print('Фантастика!!! Ошибка в функции XYZ_Efem!')
            return 0

        #####       5       #####
        # cкорость ИСЗ и геоцентрическое расстояние
        V = sqrt( x1**2 + y1**2 + z1**2)
        R = sqrt( x**2 + y**2 + z**2)

        #####       6       #####
        # постоянная энергии
        h = V**2 - 2*MU / R
        # h = MU (2/R - 1/a);

        #####       7       #####
        # большая полуось орбиты
        a = - MU / h
        # a = 1 / (2/R - V^2 / MU);

        #####       8       #####
        # Вычисляем векторы Лапласа:
        D = x*x1 + y*y1 + z*z1
        dD = MU / R + h

        f_1 = dD * x - D*x1
        f_2 = dD * y - D*y1
        f_3 = dD * z - D*z1
        f = sqrt(f_1**2 + f_2**2 + f_3**2)

        #####       9       #####
        # экстриситет орбиты ИСЗ
        e = sqrt((a-p)/a)
        if  (p > a):
            e = 0
        # e = f / MU;

        #####       10      #####
        # вычисляем аргумент перицентра
        sin_omega = f_3 / (f * sin(i))
        cos_omega = (f_1 * cos_Draco + f_2*sin_Draco) / f

        if sin_omega >= 0:
            omega = acos(cos_omega)
        elif sin_omega <= 0:
            omega = 2*pi - acos(cos_omega)
        else:
            omega = 0
            print('Фантастика!!! Ошибка в функции XYZ_Efem!')

        #####       11      #####
        # истинная аномалия:
        cos_Vi = (p - R) / (e*R)
        sin_Vi = D / (e*R) * sqrt(p/MU)
        if  sin_Vi >= 0:
            Vi = acos(cos_Vi)
        elif sin_Vi <= 0:
            Vi = 2*pi - acos(cos_Vi)
        else:
            Vi = 0
            print('Фантастика!!! Ошибка в функции XYZ_Efem!')

        #####       12      #####
        # эксцентричекая аномалия
        cos_E = (e + cos(Vi)) / (1 + e*cos(Vi))
        sin_E = (sqrt(1-e*e) * sin_Vi) / (1 + e*cos(Vi))
        if  sin_E >= 0:
            E = acos(cos_E)
        elif sin_E <= 0:
            E = 2*pi - acos(cos_E)
        else:
            print('Фантастика!!! Ошибка в функции XYZ_Efem!')
            E = 0
            sin_E = 0

        #####       13      #####
        # Эксцентрическая аномалия:
        m_0 = E - e*sin_E

        self.semimajor_axis   = a
        self.eccentricity     = e
        self.inclination      = i
        self.draco            = Draco
        self.omega            = omega
        self.M_0              = m_0


    def  ephem2xyz(self, dt):
        ''' Пересчёт эфемерид в прямоугольные координаты
        Экстраполяция координат на промежуток времени dt (секунды) вперёд
        '''
        
        a       = self.semimajor_axis
        e       = self.eccentricity
        i       = self.inclination
        Draco   = self.draco
        omega   = self.omega
        M_0     = self.M_0
        
        # вычесляем среднее движение
        n = sqrt(MU) / (a*sqrt(a))

        # вычисляем среднюю аномалию
        M = M_0 + n * dt

        # Вычисляем эксцентричекую аномалию
        E_1 = M + e * sin(M)
        E_2 = M + e * sin(E_1)
        sigma = 1e-7
        j = 2
        while  (sigma < abs(E_2 - E_1)):
            j = j+1;
            E_1 = E_2;
            E_2 = M + e * sin(E_1)
        E = E_2

        # радиус-вектор
        r = a * (1 - e*cos(E))

        # вычисление истинной аномалии:
        q = e / (1 + sqrt(1 - e**2))

        v = E + 2 * atan( (q*sin(E)) / (1 - q*cos(E)) )
        # v = 2 * atan(sqrt((1+e)/(1-e)) * tan (E/2))

        # аргумент широты
        u = omega + v

        # геоцентрическое расстояние
        # r = a * (1 - e**2) / (1 + e*cos(v));

        lll = cos(Draco)*cos(u) - sin(Draco)*sin(u)*cos(i)
        nnn = sin(Draco)*cos(u) + cos(Draco)*sin(u)*cos(i) 
        mmm = sin(u) * sin(i)
        # контроль            
        #(lnm(1)^2 + lnm(2)^2 + lnm(3)^2) 
 
        # XYZ = r * lnm;
        X = r * lll
        Y = r * nnn
        Z = r * mmm

        lll2 = -sin(u) * cos(Draco) - cos(u) * sin(Draco) * cos(i)
        nnn2 = -sin(u) * sin(Draco) + cos(u) * cos(Draco) * cos(i)
        mmm2 =  cos(u) * sin(i)
        # конроль          
        # (lnm2(1)^2 + lnm2(2)^2 + lnm2(3)^2) 

        # фокальный параметр
        P = a * (1 - e**2)

        V_r = sqrt(MU / P) * e * sin(v)
        V_t = sqrt(MU * P) / r
        # V_t = sqrt(MU/P) * (1 + e*cos(v));

        # XYZ(4:6) = V_r * lnm + V_t * lnm2;
        
        X1 = V_r * lll + V_t * lll2
        Y1 = V_r * nnn + V_t * nnn2
        Z1 = V_r * mmm + V_t * mmm2
        
        return X, Y, Z, X1, Y1, Z1


    def get_T(self):
        ''' Вычисляет и возвращает период обращения спутника
            в секундах
        '''
        a = self.semimajor_axis;
        n = sqrt(MU) / ( a * sqrt(a) )
        T = 2*pi / n
        return n


    def get_ephem(self, ephem):
        ''' возращение какого-либо элемента орбиты
        '''
        
        if ephem == 'a':
            value = self.semimajor_axis
        elif ephem == 'e':
            value = self.eccentricity
        elif ephem == 'i':
            value =  self.inclination
        elif ephem == 'd':
            value = self.draco
        elif ephem == 'w':
            value = self.omega
        else:
            value = self.M_0
            
        return value


def _test():
    print('Ку! This is test Kepler.')

    orbit = KeplerOrbit(7000, 0.1, 0.001, 0.001, 0.001, 0.1)

    print(orbit.get_T())

    orbit.dispXYZ(0)
    orbit.dispXYZ1(0)
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


if __name__ == "__main__":
    _test()