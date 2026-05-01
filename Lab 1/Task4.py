import numpy as np


# Таблица случайной согласованности (RC).
RC_TABLE = {
    1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90,
    5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41,
    9: 1.45, 10: 1.49
}


# Парсинг (поддержка дробей, например, 1/3).
def parse_number(val):
    if '/' in val:
        a, b = val.split('/')
        return float(a) / float(b)
    return float(val)


# Ввод матрицы.
def read_matrix(n, title, default_matrix):
    print(f"\nВведите {title} ({n}x{n})")
    print("Нажмите Enter, чтобы использовать матрицу по умолчанию.\n")

    matrix = []

    for i in range(n):
        line = input(f"Строка {i+1}: ").strip()

        if line == "":
            print("Используется матрица по умолчанию.\n")
            return np.array(default_matrix)

        values = line.split()

        if len(values) != n:
            print("Ошибка: неверное количество элементов.")
            return read_matrix(n, title, default_matrix)

        row = [parse_number(x) for x in values]
        matrix.append(row)

    matrix = np.array(matrix)

    # проверка обратной симметрии.
    for i in range(n):
        for j in range(n):
            if abs(matrix[i][j] * matrix[j][i] - 1) > 1e-6:
                print("Ошибка: матрица не обратносимметрична.")
                return read_matrix(n, title, default_matrix)

    return matrix


# Расчёт весов (геометрическое среднее).
def calc_priorities(matrix):
    n = matrix.shape[0]
    geom = np.prod(matrix, axis=1) ** (1 / n)
    return geom / np.sum(geom)



# Проверка согласованности (CR = CI / RC).
def check_consistency(matrix, weights):
    n = matrix.shape[0]

    V = matrix @ weights
    lam = np.mean(V / weights)

    CI = (lam - n) / (n - 1)
    RC = RC_TABLE[n]
    CR = CI / RC if RC != 0 else 0

    return lam, CI, CR


# Обработка матрицы.
def process_block(n, name, default_matrix):
    while True:
        mat = read_matrix(n, name, default_matrix)

        weights = calc_priorities(mat)
        lam, CI, CR = check_consistency(mat, weights)

        print(f"{name}:")
        print("Локальные веса:", np.round(weights, 4))
        print(f"λmax = {lam:.4f}")
        print(f"CI = {CI:.4f}")
        print(f"CR = {CR:.4f}")

        if CR <= 0.1:
            print("Матрица согласована (CR <= 0.1).\n")
            return weights
        else:
            print("Матрица несогласована (CR > 0.1). Повторите ввод.\n")


# Основная программа.
def main():
    db_list = [
        "PostgreSQL",
        "MySQL",
        "MongoDB",
        "Redis",
        "Cassandra",
        "DynamoDB"
    ]

    crit_list = [
        "Производительность",
        "Стоимость",
        "Масштабируемость",
        "Простота поддержки"
    ]

    print("Альтернативы (СУБД):")
    for i, db in enumerate(db_list):
        print(f"{i+1}. {db}")

    print("\nКритерии:")
    for i, c in enumerate(crit_list):
        print(f"{i+1}. {c}")

    # Стандартные критерии (стандартная матрица).
    default_crit = [
        [1, 3, 5, 7],
        [1/3, 1, 3, 5],
        [1/5, 1/3, 1, 3],
        [1/7, 1/5, 1/3, 1]
    ]

    # Стандартные альтернативы (стандартные матрицы).
    # Для наглядности другая матрица только у стоимости, у остальных от произв.
    default_alts = [
        # Все, кроме стоимости.
        [
            [1, 2, 4, 6, 7, 8],
            [1/2, 1, 3, 5, 6, 7],
            [1/4, 1/3, 1, 3, 5, 6],
            [1/6, 1/5, 1/3, 1, 3, 5],
            [1/7, 1/6, 1/5, 1/3, 1, 3],
            [1/8, 1/7, 1/6, 1/5, 1/3, 1]
        ],
        # Стоимость.
        [
            [1, 1/2, 1/3, 1/4, 1/5, 1/6],
            [2, 1, 1/2, 1/3, 1/4, 1/5],
            [3, 2, 1, 1/2, 1/3, 1/4],
            [4, 3, 2, 1, 1/2, 1/3],
            [5, 4, 3, 2, 1, 1/2],
            [6, 5, 4, 3, 2, 1]
        ],
    ]

    crit_weights = process_block(len(crit_list), "Матрица критериев", default_crit)

    alt_weights = []

    for i, crit in enumerate(crit_list):
        print(f"Критерий: {crit}")

        default = default_alts[i] if i < len(default_alts) else default_alts[0]

        w = process_block(len(db_list), f"Матрица альтернатив ({crit})", default)
        alt_weights.append(w)

    alt_weights = np.array(alt_weights)

    # Глобальные веса.
    global_scores = crit_weights @ alt_weights

    print("Глобальные веса (или же итог):")
    for i, db in enumerate(db_list):
        print(f"{db}: {global_scores[i]:.4f}")

    best = db_list[np.argmax(global_scores)]
    print(f"\nЛучшая СУБД: {best}")


if __name__ == "__main__":
    main()