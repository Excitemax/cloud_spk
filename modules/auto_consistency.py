#modules/auto_consistency.py
import numpy as np


def auto_fix_matrix(matrix):
    """
    Mengubah matriks menjadi konsisten menggunakan
    eigenvector method.

    Matriks baru dibentuk dari satu vektor bobot tunggal
    (aij = wi / wj). Matriks berbentuk seperti ini otomatis
    transitif sempurna, sehingga CR hasil perbaikan akan
    selalu bernilai 0 (dalam batas presisi numerik komputer),
    berapa pun input awal yang diberikan pengguna.
    """

    matrix = np.array(matrix, dtype=float)

    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError(
            "Matriks perbandingan harus berbentuk persegi "
            "(jumlah baris = jumlah kolom)."
        )

    n = matrix.shape[0]

    if n < 2:
        raise ValueError(
            "Perbaikan matriks memerlukan minimal 2 kriteria."
        )

    if np.any(matrix <= 0) or np.any(np.isnan(matrix)) or np.any(np.isinf(matrix)):
        raise ValueError(
            "Matriks mengandung nilai yang tidak valid. "
            "Semua nilai harus berupa angka positif."
        )

    eigenvalues, eigenvectors = np.linalg.eig(matrix)

    max_index = np.argmax(eigenvalues.real)

    weights = eigenvectors[:, max_index].real

    total = np.sum(weights)

    if np.isclose(total, 0.0):
        # Kasus yang secara teori nyaris tidak mungkin terjadi
        # untuk matriks reciprocal positif, tapi dijaga agar
        # tidak menghasilkan pembagian dengan nol.
        raise ValueError(
            "Perhitungan bobot eigenvector gagal (jumlah bobot "
            "mendekati nol). Periksa kembali nilai matriks input."
        )

    weights = weights / total

    # Eigenvector bisa saja seluruhnya bertanda negatif
    # (arah vektor dibalik secara matematis, hasilnya tetap
    # sah, tapi tidak bisa dibaca sebagai "bobot prioritas").
    # Baliknya tandanya agar seluruh bobot bernilai positif
    # dan bisa langsung diinterpretasikan sebagai prioritas.
    if np.sum(weights) < 0 or np.any(weights < 0):
        weights = np.abs(weights)
        weights = weights / np.sum(weights)

    consistent_matrix = np.ones((n, n))

    for i in range(n):
        for j in range(n):
            consistent_matrix[i][j] = (
                weights[i] / weights[j]
            )

    return consistent_matrix, weights