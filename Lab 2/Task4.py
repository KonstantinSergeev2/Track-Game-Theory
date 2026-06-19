import math

# Вариант 52.
lam = 0.8 # Заявок/мин.
t_service = 2.0 # Минут.
k = 3  # Число каналов.
omega = 8.0 # Интенсивность ухода из очереди.
C_revenue = 200.0 # Доход от одной обслуженной заявки (у.е.).
eps = 0.01 # Точность вычислений.

mu = 1.0 / t_service # 0.5 заявок/мин.
rho = lam / mu  # 1.6
beta = omega / mu # 16

def impatient_queue(k, rho, beta, lam, omega, eps):
    """
    Расчёт СМО с нетерпеливыми заявками.
    """
    # 1. Вычисляем p0 и вероятности состояний.
    # Сначала суммируем члены ряда для очереди (r = 1, 2, ...)
    # Пока очередной член больше eps, продолжаем.
    p0_denom = 0.0
    p_states = []
    
    # Сумма для i = 0..k (состояния без очереди).
    sum_no_queue = 0.0
    for i in range(k + 1):
        sum_no_queue += (rho ** i) / math.factorial(i)
    
    # Ряд для очереди (r >= 1).
    r = 1
    term_r = 1.0
    prod = 1.0
    queue_terms = []  # будем хранить значения слагаемых для каждого r.
    while True:
        # Вычисляем произведение (k + j*beta) для j=1..r
        if r == 1:
            prod = k + beta
        else:
            prod *= (k + r * beta)
        
  
        term = (rho ** (k + r)) / (math.factorial(k) * prod)
        queue_terms.append(term)
        
        # Если слагаемое меньше eps, прерываем цикл.
        if term < eps:
            break
        r += 1
    
    # Суммируем все члены очереди
    sum_queue = sum(queue_terms)
    
    # p0.
    p0_denom = sum_no_queue + sum_queue
    p0 = 1.0 / p0_denom
    
    # Формируем полный список вероятностей p_i
    # Сначала для i = 0..k
    p = [0.0] * (k + len(queue_terms) + 1)
    for i in range(k + 1):
        p[i] = (rho ** i / math.factorial(i)) * p0
    
    # Затем для i = k+r (r=1..len(queue_terms)).
    for idx, term in enumerate(queue_terms, start=1):
        p[k + idx] = term * p0
    
    # 2. Характеристики.
    # Среднее число занятых каналов.
    k_bar = 0.0
    for i in range(1, k + 1):
        k_bar += i * p[i]
    for r in range(1, len(queue_terms) + 1):
        k_bar += k * p[k + r]
    
    # Среднее число заявок в очереди.
    L_q = 0.0
    for r in range(1, len(queue_terms) + 1):
        L_q += r * p[k + r]
    
    # Интенсивность ухода.
    v_depart = omega * L_q
    
    # Вероятность обслуживания.
    P_serv = 1.0 - v_depart / lam
    
    # Абсолютная пропускная способность.
    A = lam * P_serv
    
    # Среднее число заявок в системе.
    L_sys = L_q + k_bar
    
    # Среднее время ожидания.
    T_q = L_q / (lam * P_serv) if P_serv > 0 else 0
    
    # Среднее время обслуживания.
    T_serv = 1.0 / mu
    
    # Среднее время пребывания.
    T_sys = T_q + T_serv
    
    # Потери дохода.
    losses = C_revenue * v_depart
    
    return {
        'p0': p0,
        'p': p,
        'k_bar': k_bar,
        'L_q': L_q,
        'L_sys': L_sys,
        'v_depart': v_depart,
        'P_serv': P_serv,
        'A': A,
        'T_q': T_q,
        'T_serv': T_serv,
        'T_sys': T_sys,
        'losses': losses
    }


res = impatient_queue(k, rho, beta, lam, omega, eps)

print(f"Исходные данные: λ = {lam} заявок/мин, t = {t_service} мин, k = {k}")
print(f"ω = {omega}, C = {C_revenue} у.е., ε = {eps}")
print(f"μ = {mu:.2f} заявок/мин, ρ = {rho:.2f}, β = {beta:.2f}")

print("\n1. Анализ работы СМО (с точностью ε = 0.01):")
print(f"   p0 = {res['p0']:.5f}")
print("   Предельные вероятности состояний (первые 10):")
for i in range(min(10, len(res['p']))):
    print(f"     p{i} = {res['p'][i]:.5f}")
if len(res['p']) > 10:
    print("   ...")

print(f"\n   Среднее число занятых каналов = {res['k_bar']:.4f}")
print(f"   Среднее число заявок в очереди L_оч = {res['L_q']:.4f}")
print(f"   Среднее число заявок в системе L_сист = {res['L_sys']:.4f}")
print(f"   Интенсивность ухода из очереди v_уход = {res['v_depart']:.4f} заявок/мин")
print(f"   Вероятность обслуживания P_обсл = {res['P_serv']:.4f} ({res['P_serv']*100:.2f}%)")
print(f"   Абсолютная пропускная способность A = {res['A']:.4f} заявок/мин")
print(f"   Среднее время ожидания T_оч = {res['T_q']:.4f} мин")
print(f"   Среднее время обслуживания T_об = {res['T_serv']:.4f} мин")
print(f"   Среднее время пребывания T_сист = {res['T_sys']:.4f} мин")

print("\n2. Потери дохода от ухода заявок из очереди:")
print(f"   Потери = C · v_уход = {C_revenue} · {res['v_depart']:.4f} = {res['losses']:.2f} у.е./мин")