# utils/matrix_helper.py
"""
Pembentukan matriks perbandingan berpasangan (pairwise) AHP.

pasangan dibentuk otomatis dengan itertools.combinations,
sehingga jumlah kriteria berapa pun (bukan cuma 5) akan otomatis
menghasilkan urutan pasangan yang benar, konsisten dengan urutan
slider yang dibuat get_pairwise_labels() di bawah.
"""

from itertools import combinations

import numpy as np

from config import CRITERIA


def get_pairwise_labels(criteria=None):
    """
    Menghasilkan daftar pasangan (kiri, kanan) untuk setiap
    kombinasi 2 kriteria, dalam urutan yang SAMA dengan yang
    dipakai build_pairwise_matrix(). Dipakai oleh input_page.py
    untuk membuat slider secara dinamis.

    Args:
        criteria : list[str], default = config.CRITERIA.

    Returns:
        list[tuple[str, str]] : mis. [("Biaya","Performa"), ...]
    """

    if criteria is None:
        criteria = CRITERIA

    return list(combinations(criteria, 2))


def build_pairwise_matrix(comparisons, criteria=None):
    """
    Membentuk matriks perbandingan berpasangan (n x n) dari
    nilai-nilai perbandingan yang diberikan pengguna.

    Args:
        comparisons : list[float], berisi C(n, 2) nilai
                      perbandingan, urutannya harus SAMA
                      dengan urutan dari get_pairwise_labels().
        criteria    : list[str], default = config.CRITERIA.

    Returns:
        numpy.ndarray (n x n) : matriks perbandingan berpasangan,
        diagonal = 1, dan tiap sel (j, i) = 1 / sel (i, j).

    Raises:
        ValueError jika jumlah nilai di `comparisons` tidak
        sesuai dengan jumlah pasangan yang diharapkan (n*(n-1)/2).
    """

    if criteria is None:
        criteria = CRITERIA

    n = len(criteria)
    expected = n * (n - 1) // 2

    if len(comparisons) != expected:
        raise ValueError(
            f"Jumlah nilai perbandingan ({len(comparisons)}) tidak "
            f"sesuai. Untuk {n} kriteria, dibutuhkan tepat "
            f"{expected} nilai perbandingan berpasangan."
        )

    matrix = np.ones((n, n))

    pairs = list(combinations(range(n), 2))

    for value, (i, j) in zip(comparisons, pairs):

        if value <= 0:
            raise ValueError(
                f"Nilai perbandingan antara '{criteria[i]}' dan "
                f"'{criteria[j]}' harus lebih besar dari 0 "
                f"(diterima: {value})."
            )

        matrix[i][j] = value
        matrix[j][i] = 1 / value

    return matrix