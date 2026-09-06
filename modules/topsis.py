# modules/topsis.py
"""
Perangkingan alternatif menggunakan metode TOPSIS
(Technique for Order Preference by Similarity to Ideal
Solution).

Alur singkat:
    1. Normalisasi matriks keputusan (normalisasi vektor).
    2. Kalikan dengan bobot kriteria -> matriks terbobot.
    3. Tentukan solusi ideal positif (A+) dan negatif (A-).
    4. Hitung jarak Euclidean tiap alternatif ke A+ dan A-.
    5. Hitung nilai preferensi (Ci) dan urutkan alternatif.

Catatan: seluruh kriteria pada sistem ini diperlakukan
sebagai kriteria "benefit" (semakin besar semakin baik).
Data penilaian ahli (lihat modules/cloud_data.py) sudah
disusun dengan asumsi ini, termasuk untuk kriteria Biaya.
"""

import numpy as np

from utils.validation import validate_decision_matrix, validate_weights


def normalize_matrix(decision_matrix):
    """
    Normalisasi vektor matriks keputusan, agar seluruh
    kriteria berada pada skala yang sebanding.

    Args:
        decision_matrix : array-like (n_alternatif x n_kriteria)

    Returns:
        numpy.ndarray, matriks ternormalisasi (ukuran sama).
    """

    matrix = np.array(decision_matrix, dtype=float)

    denominator = np.sqrt(np.sum(matrix ** 2, axis=0))

    if np.any(np.isclose(denominator, 0.0)):
        raise ValueError(
            "Terdapat kolom kriteria yang seluruh nilainya "
            "nol, sehingga normalisasi tidak dapat dilakukan "
            "(pembagian dengan nol)."
        )

    return matrix / denominator


def weighted_normalized_matrix(normalized_matrix, weights):
    """
    Mengalikan matriks ternormalisasi dengan bobot kriteria.

    Args:
        normalized_matrix : hasil dari normalize_matrix().
        weights           : array-like (n_kriteria,).

    Returns:
        numpy.ndarray, matriks ternormalisasi terbobot.
    """

    return normalized_matrix * weights


def calculate_ideal_solutions(weighted_matrix):
    """
    Menentukan solusi ideal positif (A+) dan negatif (A-)
    untuk setiap kriteria.

    Seluruh kriteria diperlakukan sebagai kriteria benefit,
    sehingga A+ = nilai maksimum kolom, A- = nilai minimum
    kolom.

    Args:
        weighted_matrix : hasil dari weighted_normalized_matrix().

    Returns:
        tuple (ideal_positive, ideal_negative), masing-masing
        numpy.ndarray berukuran (n_kriteria,).
    """

    ideal_positive = np.max(weighted_matrix, axis=0)
    ideal_negative = np.min(weighted_matrix, axis=0)

    return ideal_positive, ideal_negative


def calculate_separation(weighted_matrix, ideal_positive, ideal_negative):
    """
    Menghitung jarak Euclidean tiap alternatif terhadap
    solusi ideal positif (D+) dan negatif (D-).

    Returns:
        tuple (d_positive, d_negative), masing-masing
        numpy.ndarray berukuran (n_alternatif,).
    """

    d_positive = np.sqrt(np.sum((weighted_matrix - ideal_positive) ** 2, axis=1))
    d_negative = np.sqrt(np.sum((weighted_matrix - ideal_negative) ** 2, axis=1))

    return d_positive, d_negative


def calculate_preference_value(d_positive, d_negative):
    """
    Menghitung nilai preferensi (Ci) tiap alternatif.

    Ci mendekati 1 berarti alternatif sangat dekat dengan
    solusi ideal positif (semakin baik).

    Returns:
        numpy.ndarray, nilai preferensi tiap alternatif.

    Raises:
        ValueError jika (D+ + D-) = 0 untuk suatu alternatif
        (kasus degenerate, mis. seluruh alternatif identik).
    """

    total_distance = d_positive + d_negative

    if np.any(np.isclose(total_distance, 0.0)):
        raise ValueError(
            "Tidak dapat menghitung nilai preferensi karena "
            "jarak total (D+ + D-) bernilai nol untuk salah "
            "satu alternatif. Periksa kembali data penilaian."
        )

    return d_negative / total_distance


def rank_alternatives(preference_values, alternatives):
    """
    Mengurutkan alternatif dari nilai preferensi tertinggi
    ke terendah.

    Returns:
        list[tuple] : [(nama_alternatif, nilai_preferensi), ...]
        terurut menurun.
    """

    return sorted(
        zip(alternatives, preference_values),
        key=lambda x: x[1],
        reverse=True,
    )


def calculate_topsis(decision_matrix, weights, alternatives):
    """
    Fungsi utama TOPSIS: menjalankan seluruh tahap dari
    matriks keputusan mentah hingga ranking akhir.

    Args:
        decision_matrix : array-like (n_alternatif x n_kriteria),
                           nilai penilaian tiap alternatif pada
                           tiap kriteria.
        weights         : array-like (n_kriteria,), bobot hasil
                           Fuzzy AHP.
        alternatives    : list[str], nama tiap alternatif,
                           urutannya harus sesuai baris pada
                           decision_matrix.

    Returns:
        dict dengan key:
            "normalized_matrix" : numpy.ndarray
            "weighted_matrix"   : numpy.ndarray
            "ideal_positive"    : numpy.ndarray
            "ideal_negative"    : numpy.ndarray
            "d_positive"        : numpy.ndarray
            "d_negative"        : numpy.ndarray
            "preference"        : numpy.ndarray
            "ranking"           : list[tuple], terurut menurun

    Raises:
        ValueError jika ukuran decision_matrix, weights, atau
        alternatives tidak saling cocok, atau jika ditemukan
        data yang menyebabkan pembagian dengan nol.
    """

    n_alternatives = len(alternatives)
    n_criteria = len(weights)

    decision_matrix = validate_decision_matrix(
        decision_matrix, n_alternatives, n_criteria
    )
    weights = validate_weights(weights, n_criteria)

    normalized_matrix = normalize_matrix(decision_matrix)
    weighted_matrix = weighted_normalized_matrix(normalized_matrix, weights)

    ideal_positive, ideal_negative = calculate_ideal_solutions(weighted_matrix)

    d_positive, d_negative = calculate_separation(
        weighted_matrix, ideal_positive, ideal_negative
    )

    preference = calculate_preference_value(d_positive, d_negative)
    ranking = rank_alternatives(preference, alternatives)

    return {
        "normalized_matrix": normalized_matrix,
        "weighted_matrix": weighted_matrix,
        "ideal_positive": ideal_positive,
        "ideal_negative": ideal_negative,
        "d_positive": d_positive,
        "d_negative": d_negative,
        "preference": preference,
        "ranking": ranking,
    }