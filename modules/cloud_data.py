# modules/cloud_data.py
"""
Data penilaian ahli terhadap setiap platform cloud, dipakai
sebagai matriks keputusan pada proses TOPSIS.

Nama kriteria & alternatif diambil dari config.py (bukan
ditulis ulang di sini) supaya kalau daftar kriteria/alternatif
berubah, kesalahan penyusunan kolom akan langsung terlihat
sebagai error di validate_decision_matrix() (lihat
utils/validation.py) alih-alih menghasilkan angka yang salah
secara diam-diam.
"""

import pandas as pd

from config import CRITERIA, ALTERNATIVES

# ==========================================================
# Data mentah: rata-rata hasil penilaian 3 ahli.
#
# PENTING: urutan angka pada tiap baris HARUS mengikuti
# urutan CRITERIA di config.py. Jika CRITERIA berubah
# urutan/jumlahnya, baris-baris di bawah ini wajib
# disesuaikan secara manual (nilai ini berasal dari data
# lapangan, sehingga tidak bisa dihasilkan otomatis).
# ==========================================================

_RAW_SCORES = {
    "AWS":   [6.67, 8.67, 9.00, 9.00, 8.67],
    "GCP":   [6.33, 8.33, 8.33, 8.33, 8.00],
    "Azure": [5.00, 7.67, 7.00, 8.67, 7.33],
    "OCI":   [7.00, 7.00, 6.67, 8.00, 7.00],
}


def get_cloud_data():
    """
    Mengambil matriks keputusan TOPSIS berdasarkan hasil
    rata-rata penilaian ahli.

    Returns:
        pandas.DataFrame, index = nama platform (config.ALTERNATIVES),
        kolom = nama kriteria (config.CRITERIA).

    Raises:
        ValueError jika _RAW_SCORES tidak sinkron dengan
        config.CRITERIA / config.ALTERNATIVES (mis. jumlah
        nilai per baris tidak sama dengan jumlah kriteria).
    """

    for platform, scores in _RAW_SCORES.items():
        if len(scores) != len(CRITERIA):
            raise ValueError(
                f"Data penilaian untuk '{platform}' memiliki "
                f"{len(scores)} nilai, tetapi config.CRITERIA "
                f"berisi {len(CRITERIA)} kriteria. Periksa "
                "kembali kesesuaian modules/cloud_data.py "
                "dengan config.py."
            )

    missing = set(ALTERNATIVES) - set(_RAW_SCORES.keys())
    if missing:
        raise ValueError(
            f"Data penilaian belum tersedia untuk platform: "
            f"{', '.join(missing)}."
        )

    data = {
        criteria_name: [
            _RAW_SCORES[platform][i] for platform in ALTERNATIVES
        ]
        for i, criteria_name in enumerate(CRITERIA)
    }

    return pd.DataFrame(data, index=ALTERNATIVES)