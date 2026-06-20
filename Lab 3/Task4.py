import numpy as np

def solve_equipment_replacement():
    # Problem parameters.
    N = 5
    T_max = 5
    t0 = 2

    # Profit and cost functions.
    def R(t):
        return 25 - 2 * t if t <= T_max else 0

    def C(t):
        return 4 + 3 * t

    # DP tables: F[k][t] = max profit for k remaining years, starting with age t.
    F = np.zeros((N + 1, T_max + 1))
    policy = np.empty((N + 1, T_max + 1), dtype='U1')  # 'K' or 'R'.

    # Base case: k = 1 (last year).
    for t in range(T_max + 1):
        keep = R(t)
        replace = R(0) - C(t)
        if keep >= replace:
            F[1][t] = keep
            policy[1][t] = 'K'
        else:
            F[1][t] = replace
            policy[1][t] = 'R'

    # Recursive steps: k = 2..N.
    for k in range(2, N + 1):
        for t in range(T_max + 1):
            # Keep: profit this year + optimal from age t+1.
            next_age_keep = t + 1
            future_keep = F[k-1][next_age_keep] if next_age_keep <= T_max else 0
            keep_val = R(t) + future_keep

            # Replace: profit this year (new microservice) + optimal from age 1.
            future_replace = F[k-1][1] if 1 <= T_max else 0
            replace_val = R(0) - C(t) + future_replace

            if keep_val >= replace_val:
                F[k][t] = keep_val
                policy[k][t] = 'K'
            else:
                F[k][t] = replace_val
                policy[k][t] = 'R'

    # Print DP tables.
    print("Bellman value table F_k(t):")
    print("t   " + "   ".join([f"F{k}(t)" for k in range(1, N+1)]))
    for t in range(T_max + 1):
        row = [f"{F[k][t]:6.0f}" for k in range(1, N+1)]
        print(f"{t}   " + "   ".join(row))

    print("\nPolicy table (K=Keep, R=Replace):")
    print("t   " + "   ".join([f"pi{k}" for k in range(1, N+1)]))
    for t in range(T_max + 1):
        row = [policy[k][t] for k in range(1, N+1)]
        print(f"{t}   " + "   ".join(row))

    # Recover optimal trajectory for t0 = 2.
    print(f"\nOptimal trajectory for t0 = {t0}:")
    current_age = t0
    total_profit = 0
    trajectory = []

    for year in range(1, N + 1):
        k = N - year + 1
        action = policy[k][current_age]
        if action == 'K':
            profit = R(current_age)
            next_age = current_age + 1
        else:  # Replace.
            profit = R(0) - C(current_age)
            next_age = 1
        trajectory.append((year, current_age, action, profit, next_age))
        total_profit += profit
        current_age = next_age

    print("Year   Age   Action   Profit   Next age")
    for year, age, action, profit, next_age in trajectory:
        print(f"{year:<5} {age:<5} {action:<8} {profit:<8.0f} {next_age:<8}")

    print(f"\nMaximum total profit F_{N}({t0}) = {F[N][t0]:.0f}")
    print(f"Verified cash flow: {total_profit:.0f}")

if __name__ == "__main__":
    solve_equipment_replacement()