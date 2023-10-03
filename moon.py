from matplotlib.pyplot import *
from numpy import *

R1=1.496*10**8#Числовые данные для расчётов взяты из  публикации [6]
T1=3.156*10**7
R2=3.844*10**5
T2=2.36*10**6
N=1000.0
k1=2*pi/T1
k2=2*pi/T2
def Vx(t):
         return -k1*R1*sin(k1*t)
def Vy(t):
         return k1*R1*cos(k1*t)
def vx(t):
         return -k2*R2*sin(k2*t)
def vy(t):
         return k2*R2*cos(k2*t)
def D(t):
         return sqrt(Vx(t)**2+Vy(t)**2)-sqrt(vx(t)**2+vy(t)**2)*(Vx(t)*vx(t)+Vy(t)*vy(t))/((sqrt(Vx(t)**2+Vy(t)**2))*(sqrt(vx(t)**2+vy(t)**2)))
x=[T1*i/N for i in arange(0,N,1)]
y=[D(t) for t in x]
title("Луна движется в  одном направлении с Землёй \n Радиус орбиты  Луны  R2=3.844*10**5 км.")
xlabel('t')
ylabel('D(t)')
plot(x,y)
show()