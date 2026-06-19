import math

# Вариант 52.
lam = 3.0 # Заявок в час.
t_service_min = 1.0 # Минут на одну заявку.
k = 15  # Число каналов.
n = 3  # Число мест в очереди.
T_work = 8.0 # Время работы (часы).
C_cost = 100.0 # стоимость обслуживания одной заявки (у.е.)

# Пересчёт в часовые единицы
mu = 60 / t_service_min # 60 заявок/час
rho = lam / mu # 0.05
psi = rho / k # 0.003333

def limited_queue(k, n, rho, lam):
    """
    Расчёт многоканальной СМО с ограниченной очередью.
    k – число каналов, n – число мест в очереди.
    """
    psi = rho / k
    
    # Вычисление p0
    # Первое слагаемое.
    znam1 = 0.0
    for i in range(k + 1):
        znam1 += (rho ** i) / math.factorial(i)
    
    # Второе слагаемое: (rho^k / k!) * (1 - psi^(n+1)) / (1 - psi)
    # В данном случае psi < 1, поэтому проверка на psi == 1 не нужна
    znam2 = (rho ** k) / math.factorial(k) * (1 - psi ** (n + 1)) / (1 - psi)
    
    p0 = 1.0 / (znam1 + znam2)
    
    # Вероятности состояний.
    max_i = k + n
    p = [0.0] * (max_i + 1)
    for i in range(k + 1):
        p[i] = (rho ** i / math.factorial(i)) * p0
    for i in range(k + 1, max_i + 1):
        p[i] = (rho ** i) / (math.factorial(k) * (k ** (i - k))) * p0
    
    # Характеристики.
    p_otk = p[k + n] # Вероятность отказа.
    Q = 1 - p_otk # Относительная пропускная способность.
    A = lam * Q  # Абсолютная пропускная способность.
    
    # Среднее число заявок в очереди.
    L_q = (rho ** (k + 1)) / (k * math.factorial(k)) * (1 - (n + 1) * psi ** n + n * psi ** (n + 1)) / ((1 - psi) ** 2) * p0
    
    L_ob = rho * Q # Среднее число заявок под обслуживанием.
    L_sys = L_q + L_ob # Среднее число заявок в системе.
    
    T_ob = 1.0 / mu # Среднее время обслуживания.
    T_q = L_q / (lam * Q) if Q > 0 else 0 # Среднее время ожидания.
    T_sys = T_q + T_ob # Среднее время пребывания в системе
    
    return {
        'p0': p0,
        'p': p,
        'p_otk': p_otk,
        'Q': Q,
        'A': A,
        'L_q': L_q,
        'L_ob': L_ob,
        'L_sys': L_sys,
        'T_q': T_q,
        'T_ob': T_ob,
        'T_sys': T_sys
    }

# Расчёт для заданных параметров.
res = limited_queue(k, n, rho, lam)

print(f"Исходные данные: λ = {lam} заявок/ч, t = {t_service_min} мин, k = {k}, n = {n}")
print(f"μ = {mu:.2f} заявок/ч, ρ = {rho:.5f}, ψ = {psi:.6f}")

print("\n1. Анализ работы СМО:")
print(f"   p0 = {res['p0']:.10f}")
print("   Предельные вероятности состояний (первые 10):")
for i in range(min(10, len(res['p']))):
    print(f"     p{i} = {res['p'][i]:.10f}")
print(f"   ...")
print(f"    p_{k+n} (вероятность отказа) = {res['p_otk']:.10f}")
print(f"    P_отк = {res['p_otk']:.10f} ({res['p_otk']*100:.6f}%)")
print(f"    Q = {res['Q']:.10f} ({res['Q']*100:.6f}%)")
print(f"    A = {res['A']:.10f} заявок/ч")
print(f"    L_оч = {res['L_q']:.10f} заявок")
print(f"    L_об = {res['L_ob']:.10f} заявок")
print(f"    L_сист = {res['L_sys']:.10f} заявок")
print(f"    T_оч = {res['T_q']:.10f} ч")
print(f"    T_об = {res['T_ob']:.10f} ч")
print(f"    T_сист = {res['T_sys']:.10f} ч")

print("\n2. Потеря выручки из-за отказов:")
S_loss = C_cost * lam * res['p_otk'] * T_work
print(f"    S_потерь = C · λ · P_отк · T = {C_cost} · {lam} · {res['p_otk']:.10f} · {T_work} = {S_loss:.10f} у.е.")