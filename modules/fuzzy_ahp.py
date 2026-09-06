# modules/fuzzy_ahp.py
"""
Perhitungan bobot kriteria menggunakan Fuzzy AHP
(metode Chang Extent Analysis).

Alur singkat:
    1. Konversi matriks AHP -> matriks Triangular Fuzzy
       Number (TFN).
    2. Hitung Synthetic Extent (Si) dari setiap baris.
    3. Defuzzifikasi (Center of Area) -> nilai crisp.
    4. Normalisasi -> bobot akhir tiap kriteria (jumlah = 1).
"""

from utils.fuzzy_converter import get_tfn
from utils.validation import validate_square_positive_matrix


def convert_matrix_to_tfn(matrix):
    """
    Mengubah setiap elemen matriks AHP menjadi Triangular
    Fuzzy Number (TFN) berbentuk (l, m, u).

    Args:
        matrix : matriks perbandingan berpasangan (n x n),
                 sudah konsisten (CR < ambang batas) atau
                 hasil perbaikan otomatis.

    Returns:
        list[list[tuple]] : matriks TFN berukuran n x n,
        setiap elemen berupa tuple (l, m, u).
    """

    matrix = validate_square_positive_matrix(
        matrix, nama="Matriks Fuzzy AHP"
    )

    return [
        [get_tfn(matrix[i][j]) for j in range(matrix.shape[1])]
        for i in range(matrix.shape[0])
    ]


def calculate_fuzzy_synthetic_extent(tfn_matrix):
    """
    Menghitung nilai Synthetic Extent (Si) per baris,
    menggunakan metode Chang Extent Analysis.

    Args:
        tfn_matrix : hasil dari convert_matrix_to_tfn().

    Returns:
        list[tuple] : nilai (l, m, u) synthetic extent
        untuk setiap kriteria (baris).
    """

    row_sums = [
        (
            sum(item[0] for item in row),
            sum(item[1] for item in row),
            sum(item[2] for item in row),
        )
        for row in tfn_matrix
    ]

    total_l = sum(l for l, m, u in row_sums)
    total_m = sum(m for l, m, u in row_sums)
    total_u = sum(u for l, m, u in row_sums)

    # Perkalian silang (l dengan 1/u, dst.) sesuai definisi
    # Chang Extent Analysis: Si = row_sum x (total_sum)^-1
    return [
        (l / total_u, m / total_m, u / total_l)
        for l, m, u in row_sums
    ]


def defuzzification(fuzzy_weights):
    """
    Mengubah nilai fuzzy (l, m, u) menjadi nilai crisp
    tunggal menggunakan metode Center of Area (COA).

    Args:
        fuzzy_weights : list[tuple], hasil dari
                        calculate_fuzzy_synthetic_extent().

    Returns:
        list[float] : nilai crisp untuk tiap kriteria.
    """

    return [(l + m + u) / 3 for l, m, u in fuzzy_weights]


def normalize_weights(crisp_weights):
    """
    Menormalisasi bobot crisp agar jumlah seluruh bobot = 1.

    Args:
        crisp_weights : list[float], hasil dari
                        defuzzification().

    Returns:
        list[float] : bobot akhir tiap kriteria, jumlah = 1.

    Raises:
        ValueError jika total bobot crisp adalah 0 (kasus
        yang secara teori tidak mungkin terjadi untuk
        matriks AHP yang valid, tapi tetap dijaga agar
        tidak menghasilkan pembagian dengan nol).
    """

    total = sum(crisp_weights)

    if total == 0:
        raise ValueError(
            "Total bobot crisp bernilai nol, normalisasi "
            "tidak dapat dilakukan. Periksa kembali matriks "
            "input."
        )

    return [w / total for w in crisp_weights]


def calculate_fuzzy_ahp(matrix):
    """
    Fungsi utama Fuzzy AHP: menjalankan seluruh tahap dari
    matriks AHP hingga bobot akhir tiap kriteria.

    Args:
        matrix : matriks perbandingan berpasangan (n x n),
                 idealnya sudah konsisten (CR < ambang batas).

    Returns:
        dict dengan key:
            "tfn_matrix"       : list[list[tuple]]
            "synthetic_extent" : list[tuple]
            "crisp_weights"    : list[float]
            "final_weights"    : list[float] (jumlah = 1)
    """

    tfn_matrix = convert_matrix_to_tfn(matrix)
    synthetic_extent = calculate_fuzzy_synthetic_extent(tfn_matrix)
    crisp_weights = defuzzification(synthetic_extent)
    final_weights = normalize_weights(crisp_weights)

    return {
        "tfn_matrix": tfn_matrix,
        "synthetic_extent": synthetic_extent,
        "crisp_weights": crisp_weights,
        "final_weights": final_weights,
    }