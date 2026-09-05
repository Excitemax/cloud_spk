# utils/matrix_helper.py
import numpy as np

def build_pairwise_matrix(comparisons):
    """
    Membentuk matriks perbandingan berpasangan 5x5.

    comparisons harus berisi 10 nilai:

    [
        biaya_vs_performa,
        biaya_vs_skalabilitas,
        biaya_vs_keamanan,
        biaya_vs_reliability,
        performa_vs_skalabilitas,
        performa_vs_keamanan,
        performa_vs_reliability,
        skalabilitas_vs_keamanan,
        skalabilitas_vs_reliability,
        keamanan_vs_reliability
    ]
    """

    matrix = np.ones((5, 5))

    pairs = [
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 4),
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 3),
        (2, 4),
        (3, 4),
    ]

    for value, (i, j) in zip(comparisons, pairs):
        matrix[i][j] = value
        matrix[j][i] = 1 / value

    return matrix
