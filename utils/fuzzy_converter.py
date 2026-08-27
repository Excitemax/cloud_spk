# utils/fuzzy_converter.py

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
    Mengubah nilai AHP menjadi Triangular Fuzzy Number (TFN).
    """

    if value >= 1:
        return TFN_SCALE[int(value)]

    reciprocal = int(round(1 / value))

    l, m, u = TFN_SCALE[reciprocal]

    return (
        round(1 / u, 4),
        round(1 / m, 4),
        round(1 / l, 4),
    )