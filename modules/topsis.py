# modules/topsis.py

import numpy as np


def normalize_matrix(decision_matrix):
    """
    Normalisasi matriks keputusan TOPSIS.
    """

    matrix = np.array(
        decision_matrix,
        dtype=float
    )

    denominator = np.sqrt(
        np.sum(
            matrix ** 2,
            axis=0
        )
    )

    normalized_matrix = (
        matrix / denominator
    )

    return normalized_matrix


def weighted_normalized_matrix(
    normalized_matrix,
    weights
):
    """
    Matriks normalisasi terbobot.
    """

    return normalized_matrix * weights


def calculate_ideal_solutions(weighted_matrix):
    """
    Menghitung solusi ideal positif dan negatif.
    """

    benefit = [True, True, True, True, True]

    ideal_positive = []
    ideal_negative = []

    for j in range(weighted_matrix.shape[1]):

        column = weighted_matrix[:, j]

        if benefit[j]:

            ideal_positive.append(
                np.max(column)
            )

            ideal_negative.append(
                np.min(column)
            )

        else:

            ideal_positive.append(
                np.min(column)
            )

            ideal_negative.append(
                np.max(column)
            )

    return (
        np.array(ideal_positive),
        np.array(ideal_negative)
    )


def calculate_separation(
    weighted_matrix,
    ideal_positive,
    ideal_negative
):
    """
    Menghitung D+ dan D-
    """

    d_positive = np.sqrt(
        np.sum(
            (weighted_matrix - ideal_positive) ** 2,
            axis=1
        )
    )

    d_negative = np.sqrt(
        np.sum(
            (weighted_matrix - ideal_negative) ** 2,
            axis=1
        )
    )

    return d_positive, d_negative


def calculate_preference_value(
    d_positive,
    d_negative
):
    """
    Menghitung nilai preferensi TOPSIS.
    """

    return d_negative / (
        d_positive + d_negative
    )


def rank_alternatives(
    preference_values,
    alternatives
):
    """
    Ranking alternatif.
    """

    ranking = sorted(
        zip(
            alternatives,
            preference_values
        ),
        key=lambda x: x[1],
        reverse=True
    )

    return ranking


def calculate_topsis(
    decision_matrix,
    weights,
    alternatives
):
    """
    Fungsi utama TOPSIS.
    """

    normalized_matrix = normalize_matrix(
        decision_matrix
    )

    weighted_matrix = weighted_normalized_matrix(
        normalized_matrix,
        weights
    )

    ideal_positive, ideal_negative = (
        calculate_ideal_solutions(
            weighted_matrix
        )
    )

    d_positive, d_negative = (
        calculate_separation(
            weighted_matrix,
            ideal_positive,
            ideal_negative
        )
    )

    preference = calculate_preference_value(
        d_positive,
        d_negative
    )

    ranking = rank_alternatives(
        preference,
        alternatives
    )

    return {
        "normalized_matrix": normalized_matrix,
        "weighted_matrix": weighted_matrix,
        "ideal_positive": ideal_positive,
        "ideal_negative": ideal_negative,
        "d_positive": d_positive,
        "d_negative": d_negative,
        "preference": preference,
        "ranking": ranking
    }
