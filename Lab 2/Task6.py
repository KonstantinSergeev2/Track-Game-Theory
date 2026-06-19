import math

# Вариант 52.
k_channels = 3 # Число каналов (n в формуле).
n_sources = 16 # Число источников (i в формуле).
lam = 1.6 # Интенсивность от одного источника (заявок/час).
t_service = 0.2 # Среднее время обслуживания (часы).

mu = 1.0 / t_service # 5 заявок/час
rho = lam / mu # 0.32

def closed_multichannel(i, n, rho):
    """
    Расчёт замкнутой многоканальной СМО.
    i – число источников, n – число каналов, rho – приведённая интенсивность.
    """
    # 1. Вычисление p0.
    denom = 0.0
    
    # Сумма для k = 0..n (очереди нет)
    for k in range(n + 1):
        comb = math.factorial(i) / (math.factorial(i - k) * math.factorial(k))
        denom += comb * (rho ** k)
    
    # Сумма для k = n+1..i (есть очередь)
    for k in range(n + 1, i + 1):
        comb = math.factorial(i) / (math.factorial(i - k) * math.factorial(n) * (n ** (k - n)))
        denom += comb * (rho ** k)
    
    p0 = 1.0 / denom
    
    # 2. Вероятности состояний.
    p = [0.0] * (i + 1)
    for k in range(n + 1):
        comb = math.factorial(i) / (math.factorial(i - k) * math.factorial(k))
        p[k] = comb * (rho ** k) * p0
    for k in range(n + 1, i + 1):
        comb = math.factorial(i) / (math.factorial(i - k) * math.factorial(n) * (n ** (k - n)))
        p[k] = comb * (rho ** k) * p0
    
    # 3. Характеристики.
    # Среднее число занятых каналов.
    k_bar = 0.0
    for k in range(1, n + 1):
        k_bar += k * p[k]
    for k in range(n + 1, i + 1):
        k_bar += n * p[k]
    
    # Абсолютная пропускная способность.
    A = mu * k_bar
    
    # Относительная пропускная способность (все заявки обслуживаются).
    Q = 1.0
    
    # Среднее число заявок в системе.
    L_sys = 0.0
    for k in range(i + 1):
        L_sys += k * p[k]
    
    # Среднее число заявок в очереди.
    L_queue = L_sys - k_bar
    
    # Среднее число свободных каналов.
    free_channels = n - k_bar
    
    # Вероятность наличия очереди.
    P_queue = sum(p[n+1:])
    
    # Среднее время в системе (формула Литтла).
    T_sys = L_sys / A if A > 0 else 0
    
    # Среднее время в очереди.
    T_queue = L_queue / A if A > 0 else 0
    
    # Среднее время обслуживания.
    T_service = 1.0 / mu
    
    return {
        'p0': p0,
        'p': p,
        'k_bar': k_bar,
        'A': A,
        'Q': Q,
        'L_sys': L_sys,
        'L_queue': L_queue,
        'free_channels': free_channels,
        'P_queue': P_queue,
        'T_sys': T_sys,
        'T_queue': T_queue,
        'T_service': T_service
    }

res = closed_multichannel(n_sources, k_channels, rho)

print(f"Исходные данные: каналов n = {k_channels}, источников i = {n_sources}")
print(f"λ = {lam} заявок/час, t = {t_service} ч, μ = {mu} заявок/час, ρ = {rho:.4f}\n")

print("1. Предельные вероятности состояний (первые 10):")
for k in range(min(10, n_sources + 1)):
    print(f"   p{k} = {res['p'][k]:.6f}")
if n_sources > 10:
    print("   ...")

print(f"\n2. Вероятность того, что все каналы свободны:")
print(f"   p0 = {res['p0']:.6f} ({res['p0']*100:.4f}%)")

print(f"\n3. Среднее число заявок в очереди:")
print(f"   L_оч = {res['L_queue']:.6f}")

print(f"\n4. Среднее число заявок в системе:")
print(f"   L_сист = {res['L_sys']:.6f}")

print(f"\n5. Среднее число свободных каналов:")
print(f"   Свободных = {res['free_channels']:.6f}")

print(f"\n6. Среднее число занятых каналов:")
print(f"   Занятых = {res['k_bar']:.6f}")

print(f"\n7. Абсолютная пропускная способность:")
print(f"   A = {res['A']:.6f} заявок/час")

print(f"\n8. Относительная пропускная способность:")
print(f"   Q = {res['Q']:.1f} (все заявки будут обслужены)")

print(f"\n9. Вероятность наличия очереди:")
print(f"   P_оч = {res['P_queue']:.6f} ({res['P_queue']*100:.4f}%)")

print(f"\n10. Среднее время пребывания:")
print(f"    T_оч = {res['T_queue']:.6f} ч (в очереди)")
print(f"    T_об = {res['T_service']:.6f} ч (под обслуживанием)")
print(f"    T_сист = {res['T_sys']:.6f} ч (в системе)")