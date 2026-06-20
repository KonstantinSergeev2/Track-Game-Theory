import numpy as np
from scipy.optimize import linprog

def task1():
    # Objective coefficients (maximization -> minimize negative)
    c = -np.array([8, 11, 7, 14, 9, 16])

    # Inequality matrix (all <= constraints)
    A_ub = np.array([
        # DevOps hours.
        [3, 4, 2, 5, 2, 6],
        # Cloud budget.
        [2, 3, 1, 4, 1, 5],
        # Computational quotas.
        [15, 20, 10, 25, 8, 30],
        # min. critical sevices.
        # - (x1+x2+x3) <= -12  =>  x1+x2+x3 >= 12
        [-1, -1, -1, 0, 0, 0],
        # infrascructure balance.
        # - (x4+x5+x6) <= -10  =>  x4+x5+x6 >= 10
        [0, 0, 0, -1, -1, -1],
        # high-load gateway limit.
        # x2 + x4 <= 15
        [0, 1, 0, 1, 0, 0]
    ])

    b_ub = np.array([200, 140, 900, -12, -10, 15])

    # All variables are non-negative.
    bounds = [(0, None)] * 6

    # Solve using the 'highs' solver (returns dual values).
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

    if result.success:
        x_opt = result.x
        optimal_value = -result.fun
        shadow_prices = -result.ineqlin.marginals

        print("Optimal plan (x*):")
        for i, val in enumerate(x_opt, 1):
            print(f"x{i} = {val:.2f}")

        print(f"\nMaximum margin F* = {optimal_value:.2f} million rubles")
        print(f"Solver status: {result.message}")

        print("\nShadow prices (dual variables):")
        constraint_names = [
            "DevOps hours",
            "Cloud budget",
            "Computational quotas",
            "Critical services (>=12)",
            "Infrastructure balance (>=10)",
            "Gateway limit (<=15)"
        ]
        for name, price in zip(constraint_names, shadow_prices):
            print(f"  {name}: {price:.2f}")

        # Sensitivity analysis for cloud budget (+-15%)
        print("\nSensitivity analysis (cloud budget +-15%):")
        base_budget = 140
        for delta in [0.15, -0.15]:
            new_budget = base_budget * (1 + delta)
            b_ub_new = b_ub.copy()
            b_ub_new[1] = new_budget
            res = linprog(c, A_ub=A_ub, b_ub=b_ub_new, bounds=bounds, method='highs')
            print(f"  Budget = {new_budget:.1f}  ->  F* = {-res.fun:.2f},  change = {-res.fun - optimal_value:+.2f}")

    else:
        print("Optimization failed:", result.message)

if __name__ == "__main__":
    task1()