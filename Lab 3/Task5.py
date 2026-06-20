import numpy as np

def solve_resource_allocation():
    # Problem parameters.
    ALPHA = 0.6
    BETA = 0.7
    N_STEPS = 3
    X_MAX = 15
    GRID_STEP = 5.0
    Y_STEP = 2.0

    # Income functions.
    def g(Y):
        return 4 * Y + 0.05 * Y**2

    def h(X_minus_Y):
        return 3 * X_minus_Y + 0.1 * X_minus_Y**2

    def stage_cost(Y, X):
        return g(Y) + h(X - Y)

    def linear_interpolate(x_vals, y_vals, x_query):
        if x_query <= x_vals[0]:
            return y_vals[0]
        if x_query >= x_vals[-1]:
            return y_vals[-1]
        idx = np.searchsorted(x_vals, x_query) - 1
        x0, x1 = x_vals[idx], x_vals[idx + 1]
        y0, y1 = y_vals[idx], y_vals[idx + 1]
        return y0 + (x_query - x0) * (y1 - y0) / (x1 - x0)

    # State grid: 0, 5, 10, 15.
    X_grid = np.arange(0, X_MAX + GRID_STEP, GRID_STEP)

    # DP tables.
    F_tables = []
    Y_tables = []

    # k = 1: Base case.
    F1 = np.zeros_like(X_grid)
    Y1 = np.zeros_like(X_grid)

    for i, X in enumerate(X_grid):
        if X == 0:
            continue
        best_val = float('-inf')
        best_Y = 0.0
        Y_candidates = np.arange(0, X + Y_STEP, Y_STEP)
        Y_candidates = Y_candidates[Y_candidates <= X]
        for Y in Y_candidates:
            val = stage_cost(Y, X)
            if val > best_val:
                best_val = val
                best_Y = Y
        F1[i] = best_val
        Y1[i] = best_Y

    F_tables.append(F1)
    Y_tables.append(Y1)

    # k = 2, 3: Recursive steps.
    for k in range(2, N_STEPS + 1):
        Fk = np.zeros_like(X_grid)
        Yk = np.zeros_like(X_grid)
        F_prev = F_tables[-1]

        for i, X in enumerate(X_grid):
            if X == 0:
                continue
            best_val = float('-inf')
            best_Y = 0.0
            Y_candidates = np.arange(0, X + Y_STEP, Y_STEP)
            Y_candidates = Y_candidates[Y_candidates <= X]
            for Y in Y_candidates:
                immediate = stage_cost(Y, X)
                X_next = ALPHA * Y + BETA * (X - Y)
                future = linear_interpolate(X_grid, F_prev, X_next)
                total = immediate + future
                if total > best_val:
                    best_val = total
                    best_Y = Y
            Fk[i] = best_val
            Yk[i] = best_Y

        F_tables.append(Fk)
        Y_tables.append(Yk)

    # Print DP tables.
    print("DP Tables F_k(X) and Y_k(X):")
    print("X   F1   Y1   F2   Y2   F3   Y3")
    for i, X in enumerate(X_grid):
        f1, y1 = F_tables[0][i], Y_tables[0][i]
        f2, y2 = F_tables[1][i], Y_tables[1][i]
        f3, y3 = F_tables[2][i], Y_tables[2][i]
        print(f"{X:2.0f} {f1:5.2f} {y1:4.1f} {f2:6.2f} {y2:4.1f} {f3:6.2f} {y3:4.1f}")

    # Recover optimal trajectory for Z = 15.
    print(f"\nOptimal trajectory for Z = 15:")
    X_current = 15.0
    total_income = 0

    for k in range(N_STEPS, 0, -1):
        Y_table = Y_tables[k-1]
        Y_opt = linear_interpolate(X_grid, Y_table, X_current)
        immediate = stage_cost(Y_opt, X_current)
        X_next = ALPHA * Y_opt + BETA * (X_current - Y_opt)
        step = N_STEPS - k + 1
        print(f"Quarter {step}: X_start={X_current:6.2f}, Y*={Y_opt:6.2f}, "
              f"income={immediate:6.2f}, X_next={X_next:6.2f}")
        total_income += immediate
        X_current = X_next

    print(f"\nMaximum total income F_{N_STEPS}(15) = {F_tables[2][-1]:.2f}")
    print(f"Verified cash flow: {total_income:.2f}")

if __name__ == "__main__":
    solve_resource_allocation()