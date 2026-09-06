# utils/validation.py
# ==========================================================
# Kumpulan fungsi validasi input yang dipakai bersama oleh
# beberapa modul (consistency, auto_consistency, fuzzy_ahp,
# topsis).
#
# Tujuannya supaya:
# 1. Tidak ada kode validasi yang diulang-ulang di banyak
#    file (DRY - Don't Repeat Yourself).
# 2. Kalau ada input yang salah, pesan errornya konsisten
#    dan mudah dipahami di semua bagian sistem.
# ==========================================================

import numpy as np


def validate_square_positive_matrix(matrix, nama="Matriks"):
    """
    Memastikan `matrix` adalah matriks persegi dengan
    seluruh nilai positif, tanpa NaN/infinity.

    Dipakai untuk memvalidasi matriks perbandingan
    berpasangan (AHP) sebelum diproses lebih lanjut.

    Args:
        matrix : array-like, akan diubah ke numpy array.
        nama   : nama matriks untuk ditampilkan di pesan
                 error (mis. "Matriks perbandingan").

    Returns:
        numpy.ndarray (float) yang sudah divalidasi.

    Raises:
        ValueError jika matriks tidak valid.
    """

    matrix = np.array(matrix, dtype=float)

    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError(
            f"{nama} harus berbentuk persegi "
            "(jumlah baris = jumlah kolom)."
        )

    if matrix.shape[0] < 1:
        raise ValueError(
            f"{nama} tidak boleh kosong."
        )

    if np.any(matrix <= 0):
        raise ValueError(
            f"Semua nilai dalam {nama.lower()} harus "
            "bernilai positif (lebih besar dari 0)."
        )

    if np.any(np.isnan(matrix)) or np.any(np.isinf(matrix)):
        raise ValueError(
            f"{nama} mengandung nilai yang tidak valid "
            "(kosong/NaN atau tak terhingga)."
        )

    return matrix


def validate_decision_matrix(decision_matrix, n_alternatives, n_criteria):
    """
    Memastikan matriks keputusan TOPSIS berukuran sesuai
    dengan jumlah alternatif (baris) dan kriteria (kolom)
    yang diharapkan.

    Args:
        decision_matrix : array-like, nilai penilaian
                          setiap alternatif pada setiap
                          kriteria.
        n_alternatives  : jumlah alternatif yang diharapkan
                          (jumlah baris).
        n_criteria      : jumlah kriteria yang diharapkan
                          (jumlah kolom).

    Returns:
        numpy.ndarray (float) yang sudah divalidasi.

    Raises:
        ValueError jika ukuran atau isi matriks tidak sesuai.
    """

    matrix = np.array(decision_matrix, dtype=float)

    if matrix.ndim != 2:
        raise ValueError(
            "Matriks keputusan harus berbentuk dua dimensi "
            "(baris = alternatif, kolom = kriteria)."
        )

    if matrix.shape != (n_alternatives, n_criteria):
        raise ValueError(
            "Ukuran matriks keputusan tidak sesuai. "
            f"Diharapkan {n_alternatives} baris (alternatif) x "
            f"{n_criteria} kolom (kriteria), tetapi menerima "
            f"{matrix.shape[0]} baris x {matrix.shape[1]} kolom."
        )

    if np.any(np.isnan(matrix)) or np.any(np.isinf(matrix)):
        raise ValueError(
            "Matriks keputusan mengandung nilai yang tidak "
            "valid (kosong/NaN atau tak terhingga)."
        )

    return matrix


def validate_weights(weights, n_criteria):
    """
    Memastikan daftar bobot kriteria berjumlah sesuai
    jumlah kriteria dan bernilai positif.

    Args:
        weights    : array-like, bobot tiap kriteria.
        n_criteria : jumlah kriteria yang diharapkan.

    Returns:
        numpy.ndarray (float) yang sudah divalidasi.

    Raises:
        ValueError jika jumlah atau isi bobot tidak sesuai.
    """

    weights = np.array(weights, dtype=float)

    if weights.ndim != 1 or len(weights) != n_criteria:
        raise ValueError(
            f"Jumlah bobot kriteria ({len(weights)}) tidak "
            f"sesuai dengan jumlah kriteria ({n_criteria})."
        )

    if np.any(weights < 0):
        raise ValueError(
            "Bobot kriteria tidak boleh bernilai negatif."
        )

    if np.isclose(np.sum(weights), 0.0):
        raise ValueError(
            "Total bobot kriteria tidak boleh nol."
        )

    return weights