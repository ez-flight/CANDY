import math


def calc_lamda (Fd, Lam, ay, Rs, Vs, R_0, R_e, R_s, V_s):

    We = 7.2292115E-5

    X_s, Y_s, Z_s = Rs
    Vx_s, Vy_s, Vz_s = Vs

    Q = math.acos((X_s*Vx_s+Y_s*Vy_s+Z_s*Vz_s)/R_s/V_s)
    C = R_s*V_s*math.sin(Q)

    C1 = Y_s*Vz_s-Z_s*Vy_s
    C2 = Z_s*Vx_s-X_s*Vz_s
    C3 = X_s*Vy_s-Y_s*Vx_s

    nn11 = 1/(C*R_s)*(C2*Z_s-C3*Y_s)
    nn12 = C1/C
    nn13 = X_s/R_s

    nn21 = 1/(C*R_s)*(C3*X_s-C1*Z_s)
    nn22 = C2/C
    nn23 = Y_s/R_s

    nn31 = 1/(C*R_s)*(C1*Y_s-C2*X_s)
    nn32 = C3/C
    nn33 = Z_s/R_s

    N1 = R_e*math.cos(ay)*((-Vx_s-We*Y_s)*nn11 - (Vy_s-We*X_s)*nn21 - Vz_s*nn31)
    N2 = R_e*math.cos(ay)*((-Vx_s-We*Y_s)*nn12 - (Vy_s-We*X_s)*nn22 - Vz_s*nn32)
    N0 = R_e*math.sin(ay)*((-Vx_s-We*Y_s)*nn13 - (Vy_s-We*X_s)*nn23 - Vz_s*nn33) + Lam*Fd*R_0/2 + X_s*Vx_s+Y_s*Vy_s+Z_s*Vz_s

    Lam_f = math.asin(-N0/(math.sqrt(N1**2+N2**2)))-math.atan(N1/N2)

    Lam_f = Lam_f*180./math.pi

#    if (Lam_f < 0):
#        Lam_f = 180+Lam_f

    return Lam_f


def calc_f_doplera(Lam_f, Lam, ay, Rs, Vs, R_0, R_e, R_s, V_s):
    
    We = 7.2292115E-5
    Fd = 0
    Lam_f = Lam_f * math.pi/180
    X_s, Y_s, Z_s = Rs
    Vx_s, Vy_s, Vz_s = Vs

    Q = math.acos((X_s*Vx_s+Y_s*Vy_s+Z_s*Vz_s)/R_s/V_s)
    C = R_s*V_s*math.sin(Q)

    C1 = Y_s*Vz_s-Z_s*Vy_s
    C2 = Z_s*Vx_s-X_s*Vz_s
    C3 = X_s*Vy_s-Y_s*Vx_s

    nn11 = 1/(C*R_s)*(C2*Z_s-C3*Y_s)
    nn12 = C1/C
    nn13 = X_s/R_s

    nn21 = 1/(C*R_s)*(C3*X_s-C1*Z_s)
    nn22 = C2/C
    nn23 = Y_s/R_s

    nn31 = 1/(C*R_s)*(C1*Y_s-C2*X_s)
    nn32 = C3/C
    nn33 = Z_s/R_s

    N1 = R_e*math.cos(ay)*((-Vx_s-We*Y_s)*nn11 - (Vy_s-We*X_s)*nn21 - Vz_s*nn31)
    N2 = R_e*math.cos(ay)*((-Vx_s-We*Y_s)*nn12 - (Vy_s-We*X_s)*nn22 - Vz_s*nn32)
    N0 = R_e*math.sin(ay)*((-Vx_s-We*Y_s)*nn13 - (Vy_s-We*X_s)*nn23 - Vz_s*nn33) + Lam*Fd*R_0/2 + X_s*Vx_s+Y_s*Vy_s+Z_s*Vz_s
 #   print (Lam)
    Fd = 2./Lam/R_0*(math.cos(Lam_f)*N1+math.sin(Lam_f)*N2-N0)

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
    #0.5090215203600934    -4.880767317621834e-12
 #   Lam_f = calc_lamda (Fd, Lam, ay, Rs, Vs, R_0, R_e, R_s, V_s)
    Lam_f = 90
 #  print (Lam_f)
    Fd = calc_f_doplera (Lam_f, Lam, ay, Rs, Vs, R_0, R_e, R_s, V_s)
#   if Fd == -4.880767317621834e-12:
#   print (f"Fd = {Fd:.2f}  Работает)))")
    print (Fd)


def _test_2():

    tle_1 = ["1 56756U 23074A   24029.75507617  .00007830  00000+0  37007-3 0  9997"]
    tle_2 = ["2 56756  97.4361 225.8387 0001732  73.7060 286.4365 15.19669782 37640"]

     
    #Задаем начальное время
    dt_start = datetime(2024, 2, 21, 3, 0, 0)
    #Задаем шаг по времени для прогноза
    delta = timedelta(
        days=0,
        seconds=30,
        microseconds=0,
        milliseconds=0,
        minutes=0,
        hours=0,
        weeks=0
    )
    #Задаем количество суток для прогноза
    dt_end = dt_start + timedelta(
        days=0,
        seconds=5689,
        microseconds=0,
        milliseconds=0,
        minutes=0,
        hours=0,
        weeks=0
    )

    #Координаты объекта в геодезической СК (lat,lon, alt)
    pos_t = 59.95, 30.316667, 12

    create_orbital_track_for_f_doplera (tle_1, tle_2, dt_start, dt_end, delta, pos_t)


if __name__ == "__main__":
    _test_2()
