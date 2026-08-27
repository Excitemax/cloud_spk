# modules/consistency.py

import numpy as np


RI_TABLE = {
    1: 0.00,
    2: 0.00,
    3: 0.58,
    4: 0.90,
    5: 1.12,
    6: 1.24,
    7: 1.32,
    8: 1.41,
    9: 1.45,
    10: 1.49,
}

#cari eigen value terbesar, 
# lalu hitung CI, 
# lalu hitung CR dengan membagi CI dengan RI dari tabel di atas
def calculate_lambda_max(matrix):

    eigenvalues = np.linalg.eigvals(matrix)

    return max(eigenvalues.real)

#hitung CI dengan rumus (lambda_max - n) / (n - 1)
def calculate_ci(lambda_max, n):

    return (lambda_max - n) / (n - 1)

#hitung CR dengan rumus CI / RI, dimana RI diambil dari tabel di atas berdasarkan n
def calculate_cr(ci, n):

    ri = RI_TABLE.get(n)

    if ri == 0:
        return 0

    return ci / ri

#fungsi utama untuk melakukan uji konsistensi, 
# mengembalikan lambda_max, CI, CR, dan apakah matriks konsisten atau tidak (CR < 0.1)
def consistency_test(matrix):

    n = len(matrix)

    lambda_max = calculate_lambda_max(matrix)

    ci = calculate_ci(
        lambda_max,
        n
    )

    cr = calculate_cr(
        ci,
        n
    )

    return {
        "lambda_max": lambda_max,
        "ci": ci,
        "cr": cr,
        "is_consistent": cr < 0.1
    }
    