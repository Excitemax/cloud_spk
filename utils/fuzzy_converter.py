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


def get_tfn(value):
    """
    Mengubah nilai perbandingan AHP menjadi
    Triangular Fuzzy Number (TFN).

    Nilai hasil Auto Consistency dapat berupa
    rasio kontinu, sehingga nilai tersebut
    dipetakan ke skala AHP terdekat 1-9.
    """

    # Pastikan nilai positif
    if value <= 0:
        raise ValueError(
            "Nilai perbandingan AHP harus lebih besar dari 0."
        )

    # ==========================================================
    # Nilai >= 1
    # ==========================================================

    if value >= 1:

        # Membatasi nilai ke rentang skala Saaty 1-9
        scale_value = min(
            9,
            max(
                1,
                int(round(value))
            )
        )

        return TFN_SCALE[scale_value]

    # ==========================================================
    # Nilai reciprocal (< 1)
    # ==========================================================

    reciprocal = 1 / value

    scale_value = min(
        9,
        max(
            1,
            int(round(reciprocal))
        )
    )

    l, m, u = TFN_SCALE[scale_value]

    return (
        round(1 / u, 4),
        round(1 / m, 4),
        round(1 / l, 4),
    )