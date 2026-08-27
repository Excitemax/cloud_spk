# modules/fuzzy_ahp.py

import numpy as np

from utils.fuzzy_converter import get_tfn

def convert_matrix_to_tfn(matrix):
    """
    Mengubah matriks AHP menjadi matriks TFN.
    """

    rows, cols = matrix.shape

    tfn_matrix = []

    for i in range(rows):

        row = []

        for j in range(cols):

            row.append(
                get_tfn(matrix[i][j])
            )

        tfn_matrix.append(row)

    return tfn_matrix

def calculate_fuzzy_synthetic_extent(tfn_matrix):
    """
    Menghitung nilai Synthetic Extent (Si)
    metode Chang Extent Analysis.
    """

    row_sums = []

    for row in tfn_matrix:

        l_sum = sum(item[0] for item in row)
        m_sum = sum(item[1] for item in row)
        u_sum = sum(item[2] for item in row)

        row_sums.append(
            (l_sum, m_sum, u_sum)
        )

    total_l = sum(item[0] for item in row_sums)
    total_m = sum(item[1] for item in row_sums)
    total_u = sum(item[2] for item in row_sums)

    total_inverse = (
        1 / total_u,
        1 / total_m,
        1 / total_l
    )

    synthetic_extent = []

    for l, m, u in row_sums:

        synthetic_extent.append(
            (
                l * total_inverse[0],
                m * total_inverse[1],
                u * total_inverse[2]
            )
        )

    return synthetic_extent



def defuzzification(fuzzy_weights):
    """
    Defuzzifikasi menggunakan metode Center of Area (COA).
    """

    crisp_weights = []

    for l, m, u in fuzzy_weights:

        crisp = (l + m + u) / 3

        crisp_weights.append(crisp)

    return crisp_weights

def normalize_weights(crisp_weights):
    """
    Normalisasi bobot akhir.
    """

    total = sum(crisp_weights)

    normalized_weights = []

    for weight in crisp_weights:
        normalized_weights.append(
            weight / total
        )

    return normalized_weights


def calculate_fuzzy_ahp(matrix):

    tfn_matrix = convert_matrix_to_tfn(matrix)

    synthetic_extent = calculate_fuzzy_synthetic_extent(
        tfn_matrix
    )

    crisp_weights = defuzzification(
        synthetic_extent
    )

    final_weights = normalize_weights(
        crisp_weights
    )

    return {
        "tfn_matrix": tfn_matrix,
        "synthetic_extent": synthetic_extent,
        "crisp_weights": crisp_weights,
        "final_weights": final_weights
    }
