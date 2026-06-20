import numpy as np
from typing import Tuple, List

# Problem parameters.
ALPHA = 0.3
BETA = 0.7
N_STEPS = 4
X_MAX = 12
GRID_STEP = 1.0
Y_STEP = 0.01

def stage_cost(Y: float, X: float) -> float:
    """Immediate cost: 3*Y^2 + 2*(X-Y)^2"""
    return 3 * Y**2 + 2 * (X - Y)**2

def linear_interpolate(x_vals: np.ndarray, y_vals: np.ndarray, x_query: float) -> float:
    """Linear interpolation for F_{k-1} at fractional state."""
    if x_query <= x_vals[0]:
        return y_vals[0]
    if x_query >= x_vals[-1]:
        return y_vals[-1]
    idx = np.searchsorted(x_vals, x_query) - 1
    x0, x1 = x_vals[idx], x_vals[idx + 1]
    y0, y1 = y_vals[idx], y_vals[idx + 1]
    return y0 + (x_query - x0) * (y1 - y0) / (x1 - x0)

def solve_dp() -> Tuple[np.ndarray, List[np.ndarray], List[np.ndarray]]:
    """Build DP tables F_k(X) and Y_k(X) for k=1..4."""
    X_grid = np.arange(0, X_MAX + GRID_STEP, GRID_STEP)
    F_tables, Y_tables = [], []

    # k=1: analytic solution
    F1 = 1.2 * X_grid**2
    Y1 = 0.4 * X_grid
    F_tables.append(F1)
    Y_tables.append(Y1)

    # k=2,3,4
    for k in range(2, N_STEPS + 1):
        Fk = np.zeros_like(X_grid)
        Yk = np.zeros_like(X_grid)
        F_prev = F_tables[-1]

        for i, X in enumerate(X_grid):
            if X == 0:
                Fk[i] = 0.0
                Yk[i] = 0.0
                continue

            best_val = float('inf')
            best_Y = 0.0
            Y_candidates = np.arange(0, X + Y_STEP, Y_STEP)
            for Y in Y_candidates:
                immediate = stage_cost(Y, X)
                X_next = ALPHA * Y + BETA * (X - Y)
                future = linear_interpolate(X_grid, F_prev, X_next)
                total = immediate + future
                if total < best_val:
                    best_val = total
                    best_Y = Y
            Fk[i] = best_val
            Yk[i] = best_Y

        F_tables.append(Fk)
        Y_tables.append(Yk)

    return X_grid, F_tables, Y_tables

def recover_trajectory(X_initial: float, X_grid: np.ndarray, Y_tables: List[np.ndarray]) -> List[Tuple[float, float, float]]:
    """Backward pass: recover optimal Y sequence."""
    trajectory = []
    X_current = X_initial
    for k in range(N_STEPS, 0, -1):
        Yk = Y_tables[k-1]
        Y_opt = linear_interpolate(X_grid, Yk, X_current)
        X_next = ALPHA * Y_opt + BETA * (X_current - Y_opt)
        trajectory.append((X_current, Y_opt, X_next))
        X_current = X_next
    return trajectory

if __name__ == "__main__":
    X_grid, F_tables, Y_tables = solve_dp()

    print("X | F1   Y1   | F2   Y2   | F3   Y3   | F4   Y4")
    print("-" * 80)
    for idx, X in enumerate(X_grid):
        if X == 0:
            continue
        f1, y1 = F_tables[0][idx], Y_tables[0][idx]
        f2, y2 = F_tables[1][idx], Y_tables[1][idx]
        f3, y3 = F_tables[2][idx], Y_tables[2][idx]
        f4, y4 = F_tables[3][idx], Y_tables[3][idx]
        print(f"{int(X):2d} | {f1:5.2f} {y1:5.2f} | {f2:5.2f} {y2:5.2f} | {f3:5.2f} {y3:5.2f} | {f4:5.2f} {y4:5.2f}")

    print("\nOptimal trajectory for X=12, N=4:")
    traj = recover_trajectory(12.0, X_grid, Y_tables)
    for step, (x_start, y_opt, x_next) in enumerate(traj, 1):
        print(f"Step {step}: X_start = {x_start:.2f}, Y* = {y_opt:.2f}, X_next = {x_next:.2f}")

    print(f"\nMinimum total cost F4(12) = {F_tables[3][12]:.2f}")