#modules/inconsistency_analyzer.py
import numpy as np


def find_inconsistent_pairs(matrix, criteria):

    issues = []

    n = len(matrix)

    for i in range(n):
        for j in range(i + 1, n):

            predicted = []

            for k in range(n):

                if k != i and k != j:
                    predicted.append(
                        matrix[i][k] * matrix[k][j]
                    )

            if len(predicted) == 0:
                continue

            expected = np.mean(predicted)

            actual = matrix[i][j]

            error = abs(actual - expected)

            issues.append({
                "pair": f"{criteria[i]} vs {criteria[j]}",
                "actual": actual,
                "expected": expected,
                "error": error
            })

    issues = sorted(
        issues,
        key=lambda x: x["error"],
        reverse=True
    )

    return issues