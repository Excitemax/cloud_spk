# config.py
# ==========================================================
# Tempat TUNGGAL untuk semua konstanta yang dipakai di
# seluruh bagian sistem (modules/, pages/, utils/, app.py,
# app_user.py).
#
# Kalau suatu saat perlu mengubah, misalnya:
# - menambah/mengurangi kriteria
# - mengganti daftar platform cloud
# - mengubah batas Consistency Ratio
#
# cukup ubah di SATU file ini. Tidak perlu mencari-cari
# nilai yang sama di banyak file berbeda.
# ==========================================================

# ----------------------------------------------------------
# Kriteria penilaian
# ----------------------------------------------------------

CRITERIA = [
    "Biaya",
    "Performa",
    "Skalabilitas",
    "Keamanan",
    "Reliability",
]

# ----------------------------------------------------------
# Alternatif platform cloud yang dibandingkan
# ----------------------------------------------------------

ALTERNATIVES = [
    "AWS",
    "GCP",
    "Azure",
    "OCI",
]

# ----------------------------------------------------------
# Ambang batas konsistensi AHP (Saaty)
#
# Matriks perbandingan berpasangan dianggap konsisten
# apabila Consistency Ratio (CR) < CR_THRESHOLD.
# ----------------------------------------------------------

CR_THRESHOLD = 0.10

# ----------------------------------------------------------
# Random Index (RI) - Saaty (1980)
#
# Key = jumlah kriteria (n), Value = nilai RI baku.
# Dipakai untuk menghitung CR = CI / RI.
# ----------------------------------------------------------

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

# ----------------------------------------------------------
# Skala Triangular Fuzzy Number (TFN) untuk Fuzzy AHP
#
# Key = nilai skala Saaty (1-9), Value = (l, m, u).
# ----------------------------------------------------------

TFN_SCALE = {
    1: (1, 1, 1),
    2: (1, 2, 3),
    3: (2, 3, 4),
    4: (3, 4, 5),
    5: (4, 5, 6),
    6: (5, 6, 7),
    7: (6, 7, 8),
    8: (7, 8, 9),
    9: (9, 9, 9),
}