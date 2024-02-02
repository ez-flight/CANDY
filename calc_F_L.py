import math


def calc_lamda (Fd, Lam, ay, Rs, Vs, R_0, R_s, R_e):
        
        #Здесь мы должны выставвить F Доплера, чтоб получить угол ФИ(ay)
        #Угловая скорость вращения земли радиан в секунду    
        We =  7.292115E-5

        # Растояние в километрах
        X_s, Y_s, Zs = Rs
        Vx_s, Vy_s, Vz_s = Vs
        Rs = math.sqrt((X_s**2)+(Y_s**2)+(Zs**2))
        Vs = math.sqrt((Vx_s**2)+(Vy_s**2)+(Vz_s**2))
        # Угол в радианах
        Q = math.acos(((X_s*Vx_s)+(Y_s*Vy_s)+(Zs*Vz_s))/(R_s*Vs))
        C = Rs*Vs*math.sin(Q)

        C1 = (Y_s*Vz_s) - (Zs*Vy_s)
        C2 = (Zs*Vx_s) - (X_s*Vz_s)
        C3 = (X_s*Vy_s) - (Y_s*Vx_s)

        nn11 = 1/(C*Rs)*(C2*Zs-C3*Y_s)
        nn12 = C1/C
        nn13 = X_s/Rs

        nn21 = 1/(C*Rs)*(C3*X_s-C1*Zs)
        nn22 = C2/C
        nn23 = Y_s/Rs

        nn31 = 1/(C*Rs)*(C1*Y_s-C2*X_s)
        nn32 = C3/C
        nn33 = Zs/Rs

        N1 = R_e*math.cos(ay)*((-Vx_s-(We*Y_s))*nn11-(Vy_s-(We*X_s))*nn21-(Vz_s*nn31))
        N2 = R_e*math.cos(ay)*((-Vx_s-(We*Y_s))*nn12-(Vy_s-(We*X_s))*nn22-(Vz_s*nn32))
        N0 = R_e*math.sin(ay)*((-Vx_s-(We*Y_s))*nn13-(Vy_s-(We*X_s))*nn23-(Vz_s*nn33)) + (Lam*Fd*R_0)/2 + (X_s*Vx_s)+(Y_s*Vy_s)+(Zs*Vz_s)
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

        Lamf = math.asin(-N0/(math.sqrt((N1**2)+(N2**2))))-math.atan(N1/N2)
        Lamf=Lamf*180./3.1415
        if(Lamf<0):
            Lamf=180+Lamf
        return Lamf - 90


def calk_f_doplera(Fd, y, Lam, Rs, Vs, R_0, R_s, R_e):

        We=7.2292115E-5
        f=1/298.257
        h=0
        Re=6378.140

        Rp=(1-f)*(Re+h) 
        e2=6.694385E-3
        p=42.841382
        q=42.697725         
  
        Xs, Ys, Zs = Rs
        VSx, VSy, VSz = Vs
        R_s = math.sqrt((Xs)**2+(Ys)**2+(Zs)**2)
        V_s = math.sqrt((VSx)**2+(VSy)**2+(VSz)**2)

        Gam = math.acos(((R_s**2+R_0)**2-R_e**2)/(2*R_s*R_0))
        if y <= Gam:
            Q = math.acos((Xs*VSx+Ys*VSy+Zs*VSz)/R_s/V_s)
            C = Rs*V_s*math.sin(Q)

            C1 = Ys*VSz-Zs*VSy
            C2 = Zs*VSx-Xs*VSz
            C3 = Xs*VSy-Ys*VSx

            nn11 = 1/(C*Rs)*(C2*Zs-C3*Ys)
            nn12 = C1/C
            nn13 = Xs/Rs

            nn21 = 1/(C*Rs)*(C3*Xs-C1*Zs)
            nn22 = C2/C
            nn23 = Ys/Rs

            nn31 = 1/(C*Rs)*(C1*Ys-C2*Xs)
            nn32 = C3/C
            nn33 = Zs/Rs

            Fif = math.acos(R_0*math.sin(Gam)/R_e)

            N1 = R_e*math.cos(Fif)*((-VSx-(We*Ys))*nn11-(VSy-(We*Xs))*nn21-(VSz*nn31))
            N2 = R_e*math.cos(Fif)*((-VSx-(We*Ys))*nn12-(VSy-(We*Xs))*nn22-(VSz*nn32)) + 0.000000001
            N0 = R_e*math.sin(Fif)*((-VSx-(We*Ys))*nn13-(VSy-(We*Xs))*nn23-(VSz*nn33)) + (Lam*Fd*R_0)/2+ (Xs*VSx)+(Ys*VSy)+(Zs*VSz)

            Lamf = math.asin(-N0/(math.sqrt(N1**2+N2**2)))-math.atan(N1/N2)
            Fd=2./Lam/R_0*(math.cos(Lamf)*N1+math.sin(Lamf)*N2-N0)


def _test():

        Fd=0.0      
        Lam=0.000096
        Gam = 0.3014922881313002
        Fif = 0.9424943475517047
        Rs = (463.34597230409884, -1207.8055361811378, -6768.479049206354)
        Vs = (-2.957566053472197, -6.918572395634309, 1.0336615477187714)
        R_0 = 12616.944514074316
        R_s = 6890.993567173429
        R_e = 6374.148410772227

        ugol = calc_lamda (Fd, Lam, Fif, Rs, Vs, R_0, R_s, R_e)
        if ugol == 0.5133902270129767:
            print (f"Работает)))")

if __name__ == "__main__":
    _test()
