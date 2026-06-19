import math

# Вариант 52.
lam_day = 288 # Заявок в сутки.
t_service_min = 10 # Минут на одну заявку.
alpha_cost = 0.4 # Коэффициент в функции затрат.
n_queue_prob = 2 # Число заявок в очереди для расчёта вероятности.

lam = lam_day / 24 # 12 заявок/час.
mu = 60 / t_service_min # 6 заявок/час.
rho = lam / mu # 2.0
t_service = 1 / mu # T_обсл = 1/6 часа (10 мин)

def unlimited_queue(k, rho, lam):
    """
    Расчёт многоканальной СМО с неограниченной очередью.
    """
    # Вычисление p0.
    sum1 = 0.0
    for i in range(k):
        sum1 += (rho ** i) / math.factorial(i)
    term2 = (rho ** k) / math.factorial(k) * (1.0 / (1.0 - rho / k))
    p0 = 1.0 / (sum1 + term2)

    # Вероятности состояний.
    max_i = k + 10
    p = [0.0] * (max_i + 1)
    for i in range(k):
        p[i] = (rho ** i / math.factorial(i)) * p0
    for i in range(k, max_i + 1):
        p[i] = (rho ** i) / (math.factorial(k) * (k ** (i - k))) * p0

    # Характеристики.
    L_q = (rho ** (k + 1)) / (k * math.factorial(k)) * p0 / ((1 - rho / k) ** 2)
    L_sys = L_q + rho
    T_q = L_q / lam
    T_sys = L_sys / lam

    return {
        'p0': p0,
        'p': p,
        'L_q': L_q,
        'L_sys': L_sys,
        'T_q': T_q,
        'T_sys': T_sys
    }

# 1. Минимальное число каналов (условие стационарности).
k = 1
while True:
    if rho / k < 1:
        k_min = k
        break
    k += 1

res_min = unlimited_queue(k_min, rho, lam)

print("\n1. Минимальное число каналов (условие стационарности):")
print(f"   k_min = {k_min}  (ρ/k = {rho:.2f}/{k_min} = {rho/k_min:.2f} < 1)")
print(f"   p0 = {res_min['p0']:.5f}")
print("   Предельные вероятности состояний:")
for i in range(6):
    print(f"     p{i} = {res_min['p'][i]:.5f}")
print(f"   L_оч = {res_min['L_q']:.5f} заявок")
print(f"   L_сист = {res_min['L_sys']:.5f} заявок")
print(f"   T_оч = {res_min['T_q']:.5f} ч")
print(f"   T_сист = {res_min['T_sys']:.5f} ч")

# 2. Оптимальное число каналов по функции затрат.
# C(k) = k/λ + α * T_обсл, где T_обсл = 1/μ = const.
# Минимум достигается при минимально возможном k, т.е. k_opt = k_min.
k_opt = k_min
res_opt = unlimited_queue(k_opt, rho, lam)
cost_opt = k_opt / lam + alpha_cost * t_service

print("\n2. Оптимальное число каналов по функции затрат C(k) = k/λ + α·T_обсл:")
print(f"   k_опт = {k_opt}")
print(f"   Минимальные затраты C = {cost_opt:.5f}")
print(f"   (T_обсл = {t_service:.5f} ч = const, поэтому C минимально при наименьшем k)")

# 2. Сравнение характеристик при k_min и k_opt.
print("\n3. Сравнение характеристик при k_min и k_опт:")
print(f"   Показатель   | k_min = {k_min} | k_опт = {k_opt}")
print(f"   p0           | {res_min['p0']:.5f}   | {res_opt['p0']:.5f}")
print(f"   L_оч         | {res_min['L_q']:.5f}   | {res_opt['L_q']:.5f}")
print(f"   L_сист       | {res_min['L_sys']:.5f}   | {res_opt['L_sys']:.5f}")
print(f"   T_оч (ч)     | {res_min['T_q']:.5f}   | {res_opt['T_q']:.5f}")
print(f"   T_сист (ч)   | {res_min['T_sys']:.5f}   | {res_opt['T_sys']:.5f}")
print(f"   Затраты C    | {k_min/lam + alpha_cost*t_service:.5f}   | {cost_opt:.5f}")

# 4. Вероятность, что в очереди не более n=2 заявок.
k_prob = k_opt
limit = k_prob + n_queue_prob
res_prob = unlimited_queue(k_prob, rho, lam)
prob = sum(res_prob['p'][:limit+1])

print(f"\n4. Вероятность того, что в очереди будет не более {n_queue_prob} заявок (при k = {k_prob}):")
print(f"   P(L_оч <= {n_queue_prob}) = {prob:.5f} ({prob*100:.2f}%)")