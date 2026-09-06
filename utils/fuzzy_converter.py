# utils/fuzzy_converter.py
"""
Konversi nilai skala Saaty (1-9, atau reciprocal-nya) menjadi
Triangular Fuzzy Number (TFN) berbentuk (l, m, u).

Skala TFN_SCALE didefinisikan satu kali di config.py agar
konsisten dengan bagian sistem lain yang mungkin perlu tahu
skala yang sama di masa depan.
"""

from config import TFN_SCALE


def get_tfn(value):
    """
    Mengubah nilai perbandingan AHP menjadi Triangular Fuzzy
    Number (TFN).

    Nilai hasil Auto Consistency dapat berupa rasio kontinu
    (bukan bilangan bulat 1-9), sehingga nilai tersebut
    dipetakan ke skala Saaty terdekat sebelum dicari TFN-nya.

    Args:
        value : float, nilai perbandingan AHP (harus > 0).

    Returns:
        tuple (l, m, u) : Triangular Fuzzy Number.

    Raises:
        ValueError jika value <= 0.
    """

    if value <= 0:
        raise ValueError(
            "Nilai perbandingan AHP harus lebih besar dari 0."
        )

    if value >= 1:
        scale_value = min(9, max(1, int(round(value))))
        return TFN_SCALE[scale_value]

    # Nilai reciprocal (< 1): cari skala Saaty terdekat dari
    # kebalikannya, lalu balik lagi TFN-nya.
    reciprocal = 1 / value
    scale_value = min(9, max(1, int(round(reciprocal))))
    l, m, u = TFN_SCALE[scale_value]

    return (
        round(1 / u, 4),
        round(1 / m, 4),
        round(1 / l, 4),
    )