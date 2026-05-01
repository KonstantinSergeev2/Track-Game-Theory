import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

np.set_printoptions(suppress=True, precision=4)

# 1. Генерация платёжной матрицы 11×14, элементы [-100, 100].
def generate_matrix(n=11, m=14, low=-100, high=100, seed=58):
    np.random.seed(seed)
    return np.random.randint(low, high + 1, size=(n, m))


# 2. Метод Брауна-Робинсона.
def brown_robinson(A, iterations=7000):
    n, m = A.shape
    row_cum = np.zeros(n)
    col_cum = np.zeros(m)
    row_counts = np.zeros(n)
    col_counts = np.zeros(m)

    V_lower_history = np.empty(iterations)
    V_upper_history = np.empty(iterations)

    for t in range(1, iterations + 1):
        i = np.argmax(A.sum(axis=1)) if t == 1 else np.argmax(row_cum)
        j = np.argmin(A.sum(axis=0)) if t == 1 else np.argmin(col_cum)

        row_cum += A[:, j]
        col_cum += A[i, :]
        row_counts[i] += 1
        col_counts[j] += 1

        V_lower_history[t-1] = np.min(col_cum) / t
        V_upper_history[t-1] = np.max(row_cum) / t

    strategy_A = row_counts / iterations
    strategy_B = col_counts / iterations
    v_appr = (V_lower_history[-1] + V_upper_history[-1]) / 2
    return strategy_A, strategy_B, v_appr, V_lower_history, V_upper_history

# 3. Точное решение через линейное программирование.
def LinProgramming(A):
    n, m = A.shape
    # Игрок A.
    c = np.zeros(n + 1)
    c[-1] = -1.0
    A_ub = np.hstack([-A.T, np.ones((m, 1))])
    b_ub = np.zeros(m)
    A_eq = np.ones((1, n + 1))
    A_eq[0, -1] = 0.0
    b_eq = np.array([1.0])
    bounds = [(0, None)] * n + [(None, None)]
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
                  bounds=bounds, method='highs')
    if not res.success:
        raise ValueError("ЛП для игрока A не сошлась")
    Exact_strategy_A = res.x[:n]
    v_ex = res.x[-1]

    # Игрок B.
    c = np.zeros(m + 1)
    c[-1] = 1.0
    A_ub = np.hstack([A, -np.ones((n, 1))])
    b_ub = np.zeros(n)
    A_eq = np.ones((1, m + 1))
    A_eq[0, -1] = 0.0
    b_eq = np.array([1.0])
    bounds = [(0, None)] * m + [(None, None)]
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
                  bounds=bounds, method='highs')
    if not res.success:
        raise ValueError("ЛП для игрока B не сошлась")
    Exact_strategy_B = res.x[:m]
    return Exact_strategy_A, Exact_strategy_B, v_ex

# 4. График сходимости.
def graph_convergence(V_min, V_max, v_exact=None, filename='task1_Robinson.png'):
    plt.figure(figsize=(12, 7))
    plt.plot(range(1, len(V_min)+1), V_min, label='Нижняя оценка')
    plt.plot(range(1, len(V_max)+1), V_max, label='Верхняя оценка')
    if v_exact is not None:
        plt.axhline(y=v_exact, color='purple', linestyle='--', label=f'Точная цена (ЛП) = {v_exact:.4f}')
    plt.xlabel('Итерация')
    plt.ylabel('Цена игры')
    plt.title('Сходимость метода Брауна-Робинсона')
    plt.legend()
    plt.grid(True)
    plt.savefig(filename, dpi=100, bbox_inches='tight')
    plt.show()

if __name__ == '__main__':
    A = generate_matrix()
    print("Платёжная матрица (11*14):")
    print(A)

    print("\nЗапуск метода Брауна-Робинсона (7000 итераций):")
    pA_br, pB_br, v_br, V_min, V_max = brown_robinson(A)

    print(f"\nПриближённая цена игры: {v_br:.4f}")
    print(f"Стратегия игрока A:\n{np.round(pA_br, 4)}")
    print(f"Стратегия игрока B:\n{np.round(pB_br, 4)}")
    print(f"Границы цены: [{V_min[-1]:.4f}, {V_max[-1]:.4f}]")

    print("\nТочное решение (линейное программирование):")
    try:
        Exact_strategy_A, Exact_strategy_B, v_ex = LinProgramming(A)
        print(f"Точная цена игры: {v_ex:.4f}")
        print(f"Стратегия игрока A (ЛП):\n{np.round(Exact_strategy_A, 4)}")
        print(f"Стратегия игрока B (ЛП):\n{np.round(Exact_strategy_B, 4)}")

        print("\nСравнение:")
        print(f"Абсолютная разница цен: {abs(v_br - v_ex):.6f}")
        print(f"Относительная разница: {abs(v_br - v_ex) / max(abs(v_ex), 1e-12) * 100:.4f}%")

        graph_convergence(V_min, V_max, v_ex)
    except Exception as e:
        print(f"Ошибка ЛП: {e}")
        graph_convergence(V_min, V_max)