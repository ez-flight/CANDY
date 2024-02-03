import math


def calc_lamda (Fd, Lam, ay, Rs, Vs, R_0, R_e, R_s, V_s):
        
        #Здесь мы должны выставвить F Доплера, чтоб получить угол ФИ(ay)
        #Угловая скорость вращения земли радиан в секунду
        We =  7.292115E-5

        # Растояние в километрах
        X_s, Y_s, Z_s = Rs
        Vx_s, Vy_s, Vz_s = Vs

        # Угол в радианах
        Q = math.acos(((X_s*Vx_s)+(Y_s*Vy_s)+(Z_s*Vz_s))/(R_s*V_s))
        C = R_s*V_s*math.sin(Q)

        C1 = (Y_s*Vz_s) - (Z_s*Vy_s)
        C2 = (Z_s*Vx_s) - (X_s*Vz_s)
        C3 = (X_s*Vy_s) - (Y_s*Vx_s)

        nn11 = 1/(C*R_s)*(C2*Z_s-C3*Y_s)
        nn12 = C1/C
        nn13 = X_s/R_s

        nn21 = 1/(C*R_s)*(C3*X_s-C1*Z_s)
        nn22 = C2/C
        nn23 = Y_s/R_s

        nn31 = 1/(C*R_s)*(C1*Y_s-C2*X_s)
        nn32 = C3/C
        nn33 = Z_s/R_s

        N1 = R_e*math.cos(ay)*((-Vx_s-(We*Y_s))*nn11-(Vy_s-(We*X_s))*nn21-(Vz_s*nn31))
        N2 = R_e*math.cos(ay)*((-Vx_s-(We*Y_s))*nn12-(Vy_s-(We*X_s))*nn22-(Vz_s*nn32))
        N0 = R_e*math.sin(ay)*((-Vx_s-(We*Y_s))*nn13-(Vy_s-(We*X_s))*nn23-(Vz_s*nn33)) + (Lam*Fd*R_0)/2 + (X_s*Vx_s)+(Y_s*Vy_s)+(Z_s*Vz_s)
#        print (f"N1 = {N1} \n"
#               f"N2 = {N2} \n"
#               f"N0 = {N0} \n")
        #Решение квадратного уравнения
#        a = ((N1**2)+(N2**2))
#        b = 2*N1*N0
#        c = ((N0**2)-(N2**2))
#        print (f"a = {a} \n"
#               f"b = {b} \n"
#               f"c = {c}")
#        D = (b**2)-(4*a*c)
#        x1 = (-b+math.sqrt(D))/2*a
#        x2 = (-b-math.sqrt(D))/2*a
#        print (f"D = {D} \n"
#               f"b = {b} \n"
#               f"c = {c}")
#        if abs(x1) <= 1:
#                print (f"               {abs(x1)}")
#              print (f"               {math.acos(x1)}")
 #       if abs(x2) <=1:
#        print (f"                               {abs(x2)}")
#              print (f"                               {math.acos(x2)}")
        
        Lam_f = math.asin(-N0/(math.sqrt((N1**2)+(N2**2))))-math.atan(N1/N2)
        Fd=2./(Lam*R_0* (math.cos(Lam_f)*N1 + (math.sin(Lam_f)*N2) - N0))
        print (f"{Fd:.2f}")
        Lam_f=Lam_f*180./3.1415
        if(Lam_f<0):
            Lam_f= 180 + Lam_f
        Lam_f = Lam_f - 90
  #      print (f"{Lam_f}    {Fd}")
        return Lam_f


def calc_f_doplera(Lam_f, Lam, ay, Rs, Vs, R_0, R_e, R_s, V_s):
        
        #Здесь мы должны выставвить F Доплера, чтоб получить угол ФИ(ay)
        #Угловая скорость вращения земли радиан в секунду
        We =  7.292115E-5
        Fd = 0

 #       Lam_f = Lam_f*3.1415/180

        # Растояние в километрах
        X_s, Y_s, Z_s = Rs
        Vx_s, Vy_s, Vz_s = Vs

        # Угол в радианах
        Q = math.acos(((X_s*Vx_s)+(Y_s*Vy_s)+(Z_s*Vz_s))/(R_s*V_s))
        C = R_s*V_s*math.sin(Q)

        C1 = (Y_s*Vz_s) - (Z_s*Vy_s)
        C2 = (Z_s*Vx_s) - (X_s*Vz_s)
        C3 = (X_s*Vy_s) - (Y_s*Vx_s)

        nn11 = 1/(C*R_s)*(C2*Z_s-C3*Y_s)
        nn12 = C1/C
        nn13 = X_s/R_s

        nn21 = 1/(C*R_s)*(C3*X_s-C1*Z_s)
        nn22 = C2/C
        nn23 = Y_s/R_s

        nn31 = 1/(C*R_s)*(C1*Y_s-C2*X_s)
        nn32 = C3/C
        nn33 = Z_s/R_s

        N1 = R_e*math.cos(ay)*((-Vx_s-(We*Y_s))*nn11-(Vy_s-(We*X_s))*nn21-(Vz_s*nn31))
        N2 = R_e*math.cos(ay)*((-Vx_s-(We*Y_s))*nn12-(Vy_s-(We*X_s))*nn22-(Vz_s*nn32))
        N0 = R_e*math.sin(ay)*((-Vx_s-(We*Y_s))*nn13-(Vy_s-(We*X_s))*nn23-(Vz_s*nn33)) + (Lam*Fd*R_0)/2 + (X_s*Vx_s)+(Y_s*Vy_s)+(Z_s*Vz_s)


        Fd=2./(Lam*R_0)*(math.cos(Lam_f)*N1+math.sin(Lam_f)*N2-N0)
  #      Lamf = math.asin(-N0/(math.sqrt(N1**2+N2**2)))-math.atan(N1/N2)
        return Fd


def _test():

        Fd=0.0      
        Lam=0.000096
        Gam = 0.3014922881313002
        ay = 0.9424943475517047
        Rs = (463.34597230409884, -1207.8055361811378, -6768.479049206354)
        Vs = (-2.957566053472197, -6.918572395634309, 1.0336615477187714)
        R_0 = 12616.944514074316
        R_s = 6890.993567173429
        R_e = 6374.148410772227
        V_s = 7.5948862499392655

        Lam_f = calc_lamda (Fd, Lam, ay, Rs, Vs, R_0, R_e, R_s, V_s)
        if Lam_f == 0.5133902270129767:
            print (f"Работает)))")

        Fd = calc_f_doplera (Lam_f, Lam, ay, Rs, Vs, R_0, R_e, R_s, V_s)
        print (Fd)


if __name__ == "__main__":
    _test()
