#modules/auto_consistency.py
import numpy as np

def auto_fix_matrix(matrix):
    """
    Mengubah matriks menjadi konsisten menggunakan
    eigenvector method.
    """

    eigenvalues, eigenvectors = np.linalg.eig(matrix)

    max_index = np.argmax(eigenvalues.real)

    weights = eigenvectors[:, max_index].real

    weights = weights / np.sum(weights)

    n = len(weights)

    consistent_matrix = np.ones((n, n))

    for i in range(n):
        for j in range(n):
            consistent_matrix[i][j] = (
                weights[i] / weights[j]
            )

    return consistent_matrix, weights
