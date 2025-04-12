import math


def compute_N_terms(Rs, Vs, R_s, V_s, We, ay, Lam, Fd, R_0, R_e, debug=False):
    """
    Вычисление общих термов N1, N2, N0 для уравнений.
    Включает поправку на вращение Земли (We) и влияние Fd на N0.
    """
    X_s, Y_s, Z_s = Rs
    Vx_s, Vy_s, Vz_s = Vs

    # Скалярное произведение и угол Q
    dot_product = X_s * Vx_s + Y_s * Vy_s + Z_s * Vz_s
    denominator_acos = R_s * V_s
    if denominator_acos == 0:
        raise ValueError("R_s или V_s равно нулю")
    Q = math.acos(dot_product / denominator_acos)
    sin_Q = math.sin(Q)
    C = R_s * V_s * sin_Q

    if C == 0:
        raise ValueError("C равно нулю")

    # Векторное произведение [Rs × Vs]
    C1 = Y_s * Vz_s - Z_s * Vy_s
    C2 = Z_s * Vx_s - X_s * Vz_s
    C3 = X_s * Vy_s - Y_s * Vx_s

    # Элементы матрицы преобразования
    inv_CRs = 1 / (C * R_s)
    nn11 = inv_CRs * (C2 * Z_s - C3 * Y_s)
    nn12 = C1 / C
    nn13 = X_s / R_s

    nn21 = inv_CRs * (C3 * X_s - C1 * Z_s)
    nn22 = C2 / C
    nn23 = Y_s / R_s

    nn31 = inv_CRs * (C1 * Y_s - C2 * X_s)
    nn32 = C3 / C
    nn33 = Z_s / R_s

    # Корректировка скоростей с учетом вращения Земли
    term_Vx = -Vx_s - We * Y_s
    term_Vy = -Vy_s + We * X_s  # Исправленный знак
    term_Vz = -Vz_s

    # Вычисление компонентов N
    N1_part = term_Vx * nn11 + term_Vy * nn21 + term_Vz * nn31
    N2_part = term_Vx * nn12 + term_Vy * nn22 + term_Vz * nn32
    N0_part = term_Vx * nn13 + term_Vy * nn23 + term_Vz * nn33

    cos_ay = math.cos(ay)
    sin_ay = math.sin(ay)

    N1 = R_e * cos_ay * N1_part
    N2 = R_e * cos_ay * N2_part
    N0 = R_e * sin_ay * N0_part + Lam * Fd * R_0 / 2 + dot_product

    if debug:
        print(f"[DEBUG] term_Vx: {term_Vx:.6f}, term_Vy: {term_Vy:.6f}, term_Vz: {term_Vz:.6f}")
        print(f"N1_part: {N1_part:.6f}, N2_part: {N2_part:.6f}, N0_part: {N0_part:.6f}")

    return N1, N2, N0

def calc_lamda(Fd, Lam, ay, Rs, Vs, R_0, R_e, R_s, V_s):
    """
    Расчет угла места λ (в градусах) с исправленной логикой:
    - Использование compute_N_terms для устранения дублирования кода
    - Замена math.atan на math.atan2 для корректного расчета угла
    - Обработка исключений для math.asin
    """
    We = 7.2292115E-5

    try:
        # Получение N1, N2, N0 через общую функцию
        N1, N2, N0 = compute_N_terms(Rs, Vs, R_s, V_s, We, ay, Lam, Fd, R_0, R_e)
        
        denominator = math.sqrt(N1**2 + N2**2)
        if denominator == 0:
            raise ValueError("N1 и N2 не могут быть одновременно нулевыми")
        
        arg = -N0 / denominator
        
        # Проверка допустимости аргумента для arcsin
        if arg < -1.0 or arg > 1.0:
            print(f"Предупреждение: Недопустимый аргумент arcsin: {arg:.6f}")
            Lam_f = math.pi / 2  # 90° по умолчанию
        else:
            Lam_f = math.asin(arg) - math.atan2(N1, N2)  # math.atan2 вместо math.atan

        # Преобразование в градусы и коррекция диапазона
        Lam_f_deg = math.degrees(Lam_f)
        if Lam_f_deg < 0:
            Lam_f_deg += 360  # Приведение к диапазону [0, 360)
        
    except ValueError as e:
        print(f"Ошибка в calc_lamda: {e}")
        Lam_f_deg = 90.0  # Значение по умолчанию

    return Lam_f_deg

def calc_f_doplera(a, Lam, ay, Rs, Vs, R_0, R_e, R_s, V_s):
    """
    Расчет доплеровской частоты (Fd) с использованием compute_N_terms.
    """
    We = 7.2292115E-5
    a_rad = math.radians(a)
    
    try:
        N1, N2, N0 = compute_N_terms(Rs, Vs, R_s, V_s, We, ay, Lam, 0.0, R_0, R_e)
        Fd = (2.0 / (Lam * R_0)) * (math.cos(a_rad) * N1 + math.sin(a_rad) * N2 - N0)
    except Exception as e:
        print(f"Ошибка в calc_f_doplera: {e}")
        Fd = 0.0
    return Fd

def _test():
    """Тест с примером из предыдущих данных пользователя"""
    Fd=0.0      
    Lam = 0.000096  # 0.096 м
    Gam = 0.3014922881313002
    ay = 0.9424943475517047  # ~54°
    Rs = (463.34597230409884, -1207.8055361811378, -6768.479049206354)
    Vs = (-2.957566053472197, -6.918572395634309, 1.0336615477187714)
    R_0 = 12616.944514074316
    R_s = 6890.993567173429
    R_e = 6374.148410772227
    V_s = 7.5948862499392655
    a = 90

    # Тест доплеровской частоты
    Fd = calc_f_doplera(a, Lam, ay, Rs, Vs, R_0, R_e, R_s, V_s)
    print(f"Fd = {Fd:.6f} Гц")  # Ожидается: Fd = -414.511315 Гц
    Fd=0.0  
    # Тест угла места
    Lam_f = calc_lamda(Fd, Lam, ay, Rs, Vs, R_0, R_e, R_s, V_s)
    print(f"λ = {Lam_f:.2f}°")  # Пример вывода: λ = 91.01°

if __name__ == "__main__":
    _test()