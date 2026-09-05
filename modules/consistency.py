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


def _validate_matrix(matrix):
    """
    Memastikan matriks yang masuk berbentuk matriks
    perbandingan berpasangan yang valid, agar fungsi-fungsi
    di bawah tidak menghasilkan error yang membingungkan
    (mis. ValueError bawaan numpy) ketika ada kesalahan input.
    """

    matrix = np.array(matrix, dtype=float)

    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError(
            "Matriks perbandingan harus berbentuk persegi "
            "(jumlah baris = jumlah kolom)."
        )

    if matrix.shape[0] < 1:
        raise ValueError(
            "Matriks tidak boleh kosong."
        )

    if np.any(matrix <= 0):
        raise ValueError(
            "Semua nilai dalam matriks perbandingan harus "
            "bernilai positif (lebih besar dari 0)."
        )

    if np.any(np.isnan(matrix)) or np.any(np.isinf(matrix)):
        raise ValueError(
            "Matriks mengandung nilai yang tidak valid "
            "(kosong/NaN atau tak terhingga)."
        )

    return matrix


# cari eigen value terbesar,
# lalu hitung CI,
# lalu hitung CR dengan membagi CI dengan RI dari tabel di atas
def calculate_lambda_max(matrix):

    matrix = _validate_matrix(matrix)

    eigenvalues = np.linalg.eigvals(matrix)

    # Untuk matriks AHP yang valid, eigenvalue terbesar
    # seharusnya bernilai real. Bagian imajiner diabaikan
    # (diambil .real) karena secara numerik selalu
    # mendekati nol untuk matriks reciprocal positif.
    return float(max(eigenvalues.real))


# hitung CI dengan rumus (lambda_max - n) / (n - 1)
def calculate_ci(lambda_max, n):

    if n <= 1:
        # Tidak ada perbandingan yang mungkin dilakukan
        # untuk 1 kriteria atau kurang, sehingga matriks
        # otomatis dianggap konsisten sempurna.
        return 0.0

    ci = (lambda_max - n) / (n - 1)

    # Pembulatan numerik kadang menghasilkan CI sedikit
    # negatif (misal -1e-16) walau seharusnya nol.
    if ci < 0:
        ci = 0.0

    return ci


# hitung CR dengan rumus CI / RI, dimana RI diambil dari tabel
# di atas berdasarkan n
def calculate_cr(ci, n):

    ri = RI_TABLE.get(n)

    if ri is None:
        raise ValueError(
            f"Jumlah kriteria (n={n}) berada di luar cakupan "
            "tabel Random Index (RI) standar Saaty (maksimum "
            "10 kriteria). Tambahkan nilai RI yang sesuai pada "
            "RI_TABLE jika ingin menggunakan lebih dari 10 kriteria."
        )

    if ri == 0:
        return 0.0

    return ci / ri


# fungsi utama untuk melakukan uji konsistensi,
# mengembalikan lambda_max, CI, CR, dan apakah matriks
# konsisten atau tidak (CR < 0.1)
def consistency_test(matrix):

    matrix = _validate_matrix(matrix)

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