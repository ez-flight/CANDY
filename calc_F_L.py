import math


def calc_lamda (Fd, Lam, Gam, Fif, Rs, Vs, R_0, R_s, R_e):
        #
        #Угловая скорость вращения земли радиан в секунду    
        We=  7.292115E-5
#        We=7.292115E-5
        
        f=1/298.257
        h=0
        # Радиус земли в Километрах
        Re=6378.140
        Rp=(1-f)*(Re+h)
        e2=6.694385E-3
        p=42.841382
        q=42.697725

        # Растояние в километрах
        Xs, Ys, Zs = Rs
        VSx, VSy, VSz = Vs
        Rs = math.sqrt((Xs**2)+(Ys**2)+(Zs**2))
        Vs = math.sqrt((VSx**2)+(VSy**2)+(VSz**2))
        # Угол в радианах
        Q = math.acos(((Xs*VSx)+(Ys*VSy)+(Zs*VSz))/(R_s*Vs))
        C = Rs*Vs*math.sin(Q)

        C1 = (Ys*VSz) - (Zs*VSy)
        C2 = (Zs*VSx) - (Xs*VSz)
        C3 = (Xs*VSy) - (Ys*VSx)

        nn11 = 1/(C*Rs)*(C2*Zs-C3*Ys)
        nn12 = C1/C
        nn13 = Xs/Rs

        nn21 = 1/(C*Rs)*(C3*Xs-C1*Zs)
        nn22 = C2/C
        nn23 = Ys/Rs

        nn31 = 1/(C*Rs)*(C1*Ys-C2*Xs)
        nn32 = C3/C
        nn33 = Zs/Rs

        N1 = R_e*math.cos(Fif)*((-VSx-(We*Ys))*nn11-(VSy-(We*Xs))*nn21-(VSz*nn31))
        N2 = R_e*math.cos(Fif)*((-VSx-(We*Ys))*nn12-(VSy-(We*Xs))*nn22-(VSz*nn32))# + 0.000000001
        N0 = R_e*math.sin(Fif)*((-VSx-(We*Ys))*nn13-(VSy-(We*Xs))*nn23-(VSz*nn33)) + (Lam*Fd*R_0)/2 + (Xs*VSx)+(Ys*VSy)+(Zs*VSz)

        Lamf = math.asin(-N0/(math.sqrt((N1**2)+(N2**2))))-math.atan(N1/N2)
        Lamf=Lamf*180./3.1415
 #       if(Lamf<0):
 #           Lamf=180+Lamf
        return Lamf


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
 #       calk_fdoplera (Fd, y, Lam, Rs, Vs, R_0, R_s, R_e)


if __name__ == "__main__":
    _test()
