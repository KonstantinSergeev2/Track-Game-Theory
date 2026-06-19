import math

# Вариант 52
alpha = 1.5 # Среднее время обслуживания (в часах)
n_day = 36 # Заявок в сутки.
k_given = 4 # Число каналов.


lam = n_day / 24 # 1.5 заявки/час
mu = 1 / alpha # 0.6667 заявки/час
rho = lam / mu # 2.25

def erlang(k, rho):
    """
    Расчёт многоканальной СМО с отказами по формулам Эрланга.
    """
    # Вычисляем p0.
    sum = 0.0
    for i in range(k + 1):
        sum += (rho ** i) / math.factorial(i)
    p0 = 1.0 / sum
    
    # Вычисляем все вероятности состояний p_i
    p = [0.0] * (k + 1)
    for i in range(k + 1):
        p[i] = (rho ** i / math.factorial(i)) * p0
    
    p_otk = p[k] # Вероятность отказа (заняты все k каналов)
    Q = 1 - p_otk # Относительная пропускная способность
    A = lam * Q # Абсолютная пропускная способность
    k_zan = rho * Q # Среднее число занятых каналов
    k_zagr = k_zan / k # Коэффициент загрузки каналов
    
    return {
        'p0': p0,
        'p': p,
        'p_otk': p_otk,
        'Q': Q,
        'A': A,
        'k_zan': k_zan,
        'k_zagr': k_zagr
    }

# 1. Минимальное k (число каналов) для Q >= 95%.
k = 1
while True:
    res = erlang(k, rho)
    if res['Q'] >= 0.95:
        k_min = k
        break
    k += 1

print("1. Минимальное число каналов для Q >= 95%")
print(f"k_min = {k_min}")
print(f"При k = {k_min}: Q = {res['Q']:.5f}, P_отк = {res['p_otk']:.5f}")

# 2. Расчёт для заданного k = 4
res_k = erlang(k_given, rho)

print("\n2-3. Характеристики для k = 4 каналов.")
print(f"Число каналов: {k_given}")
print(f"Предельные вероятности состояний:")
for i, pi in enumerate(res_k['p']):
    print(f"  p{i} = {pi:.5f}")
print(f"\nP_отк (вероятность отказа) = {res_k['p_otk']:.5f}")
print(f"Q (относительная пропускная способность) = {res_k['Q']:.5f}")
print(f"A (абсолютная пропускная способность) = {res_k['A']:.5f} заявок/час")
print(f"Среднее число занятых каналов = {res_k['k_zan']:.5f}")
print(f"Коэффициент загрузки каналов = {res_k['k_zagr']:.5f}")