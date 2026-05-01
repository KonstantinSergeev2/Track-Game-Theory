import numpy as np
from scipy.optimize import linprog

np.set_printoptions(suppress=True, precision=4)

# 1. Параметры модели безопасности.
N = 7
V = np.array([120, 95, 140, 80, 110, 60, 130]) # Ценность узлов.
C = np.array([35, 25, 40, 20, 30, 15, 45])  # Стоимость защиты узлов.
P_succ_def = 0.2 # Вероятность успеха атаки при защите.
P_succ_no_def = 0.8 # Вероятность успеха атаки без защиты.
B = 100 # Бюджет защитника.

# 2. Поиск равновесия Штакельберга.
def solve_stackelberg(N, V, C, P_succ_def, P_succ_no_def, B):
    c = np.zeros(N + 1)
    c[-1] = 1.0
    A_ub = []
    b_ub = []

    for j in range(N):
        row = np.zeros(N + 1)
        row[j] = -(P_succ_no_def - P_succ_def) * V[j]
        row[-1] = -1.0
        A_ub.append(row)
        b_ub.append(-P_succ_no_def * V[j])

    budget_row = np.zeros(N + 1)
    budget_row[:N] = C
    A_ub.append(budget_row)
    b_ub.append(B)

    for i in range(N):
        row = np.zeros(N + 1)
        row[i] = 1.0
        A_ub.append(row)
        b_ub.append(1.0)

    bounds = [(0, 1) for _ in range(N)] + [(None, None)]

    A_ub = np.array(A_ub)
    b_ub = np.array(b_ub)

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
    if not res.success:
        raise ValueError("ЛП не сошлась: " + res.message)

    p_opt = res.x[:N]
    t_opt = res.x[-1]
    expected_damage = p_opt * P_succ_def * V + (1 - p_opt) * P_succ_no_def * V
    return p_opt, t_opt, expected_damage

# 3. Расчёт и вывод.
p_opt, t_opt, damage = solve_stackelberg(N, V, C, P_succ_def, P_succ_no_def, B)

print("Оптимальные вероятности защиты:")
for i, p in enumerate(p_opt):
    print(f"  Узел {i+1}: {p:.4f}")

print(f"\nМаксимальный ожидаемый ущерб: {t_opt:.4f}")
print("Ожидаемый ущерб по узлам:", np.round(damage, 4))
max_damage = np.max(damage)
targets = [i+1 for i, d in enumerate(damage) if abs(d - max_damage) < 1e-6]
chosen = targets[0]
print(f"Атакующий выберет узел {chosen} (ценность узла: {V[chosen-1]})")