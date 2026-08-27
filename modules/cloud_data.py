# modules/cloud_data.py

import pandas as pd


def get_cloud_data():
    """
    Matriks keputusan TOPSIS berdasarkan hasil rata-rata penilaian ahli.
    """

    data = {
        "Biaya": [6.67, 6.33, 5.00, 7.00],
        "Performa": [8.67, 8.33, 7.67, 7.00],
        "Skalabilitas": [9.00, 8.33, 7.00, 6.67],
        "Keamanan": [9.00, 8.33, 8.67, 8.00],
        "Reliability": [8.67, 8.00, 7.33, 7.00],
    }

    alternatives = [
        "AWS",
        "GCP",
        "Azure",
        "OCI"
    ]

    return pd.DataFrame(data, index=alternatives)