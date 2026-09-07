#pages/input_page.py
"""
Halaman input preferensi pengguna (Tahap 1).

Sebelumnya setiap pasangan kriteria (Biaya vs Performa, Biaya
vs Skalabilitas, dst) ditulis manual satu per satu sebagai
pemanggilan fungsi terpisah. Total ada 10 pemanggilan untuk
5 kriteria - kalau kriteria bertambah jadi 6, seharusnya ada
15 pasangan, dan menulis semuanya manual sangat rawan salah
urut atau ada yang lupa ditambahkan.

Sekarang seluruh pasangan dibuat otomatis dari config.CRITERIA
lewat matrix_helper.get_pairwise_labels(), sehingga jumlah
kriteria berapa pun akan otomatis menghasilkan slider yang
sesuai, tanpa mengubah kode di file ini.
"""

import streamlit as st
import numpy as np

from config import CRITERIA
from utils.matrix_helper import get_pairwise_labels, build_pairwise_matrix


# ==========================================================
# Pemetaan posisi slider (-8 s.d. 8) ke nilai skala Saaty.
# Didefinisikan sekali di sini karena dipakai berkali-kali
# oleh pairwise_slider().
# ==========================================================

_POSITION_TO_SAATY = {
    -8: 9, -7: 8, -6: 7, -5: 6, -4: 5, -3: 4, -2: 3, -1: 2,
     0: 1,
     1: 1/2, 2: 1/3, 3: 1/4, 4: 1/5, 5: 1/6, 6: 1/7, 7: 1/8, 8: 1/9,
}

_POSITION_TO_LABEL = {
    -8: "mutlak lebih penting",
    -7: "berada di antara sangat dan mutlak lebih penting",
    -6: "sangat lebih penting",
    -5: "berada di antara lebih penting dan sangat lebih penting",
    -4: "lebih penting",
    -3: "berada di antara sedikit dan lebih penting",
    -2: "sedikit lebih penting",
    -1: "berada di antara sama dan sedikit lebih penting",
     0: "__SAMA__",
     1: "berada di antara sama dan sedikit lebih penting",
     2: "sedikit lebih penting",
     3: "berada di antara sedikit dan lebih penting",
     4: "lebih penting",
     5: "berada di antara lebih penting dan sangat lebih penting",
     6: "sangat lebih penting",
     7: "berada di antara sangat dan mutlak lebih penting",
     8: "mutlak lebih penting",
}


def pairwise_slider(label, first, second):
    """
    Menampilkan satu slider perbandingan berpasangan antara
    dua kriteria (`first` vs `second`), dan mengembalikan
    nilai skala Saaty hasil pilihan pengguna.

    Args:
        label  : key unik untuk widget Streamlit (mis. hasil
                 gabungan "Biaya vs Performa").
        first  : nama kriteria di sisi kiri slider.
        second : nama kriteria di sisi kanan slider.

    Returns:
        float : nilai skala Saaty (1-9, atau reciprocal-nya).
    """

    st.markdown(f"**{label}**")

    st.markdown(
        f"""
        <div style="display:flex;
                    justify-content:space-between;
                    font-weight:bold;
                    margin-bottom:5px;">
            <span>{first}</span>
            <span>{second}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style='display:flex;
                    justify-content:space-between;
                    font-size:12px;'>
            <span>9</span><span>8</span><span>7</span><span>6</span>
            <span>5</span><span>4</span><span>3</span><span>2</span>
            <span>1</span>
            <span>2</span><span>3</span><span>4</span><span>5</span>
            <span>6</span><span>7</span><span>8</span><span>9</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style='display:flex;
                    justify-content:space-between;
                    font-size:11px;
                    color:gray;
                    margin-bottom:5px;'>
            <span>← {first} lebih penting</span>
            <span>{second} lebih penting →</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    position = st.slider(
        "",
        min_value=-8,
        max_value=8,
        value=0,
        step=1,
        label_visibility="collapsed",
        key=label
    )

    if position == 0:
        st.caption("Kedua kriteria sama penting")
    elif position < 0:
        st.caption(f"{first} {_POSITION_TO_LABEL[position]}")
    else:
        st.caption(f"{second} {_POSITION_TO_LABEL[position]}")

    return _POSITION_TO_SAATY[position]


def show_input(mode="teknis"):
    """
    Menampilkan seluruh slider preferensi kriteria (dibuat
    otomatis dari config.CRITERIA) dan membentuk matriks
    perbandingan berpasangan dari hasil input pengguna.

    Args:
        mode : "teknis" (default) menampilkan istilah AHP
               (nilai AHP, Consistency Ratio/CR, Auto
               Consistency, Fuzzy AHP) - dipakai di app.py
               untuk keperluan sidang/demo.

               "awam" menampilkan bahasa yang sama sekali
               tidak menyebut istilah teknis di atas - dipakai
               di app_user.py untuk pengguna akhir.

    Returns:
        tuple (matrix_user, criteria)
            matrix_user : numpy.ndarray (n x n)
            criteria    : list[str], selalu config.CRITERIA
    """

    st.header("Input Preferensi Kriteria")

    st.info("""
    Geser slider untuk menentukan tingkat kepentingan antar dua kriteria.

    • Geser ke kiri apabila kriteria di sebelah kiri lebih diprioritaskan.

    • Geser ke kanan apabila kriteria di sebelah kanan lebih diprioritaskan.

    • Posisi tengah menunjukkan kedua kriteria memiliki tingkat kepentingan yang sama.
    """)

    if mode == "teknis":

        with st.expander("Lihat Konversi Pilihan ke Nilai AHP"):

            st.markdown("""
            Nilai AHP | Makna

            9 | Mutlak lebih penting

            8 | Nilai kompromi

            7 | Sangat lebih penting

            6 | Nilai kompromi

            5 | Lebih penting

            4 | Nilai kompromi

            3 | Sedikit lebih penting

            2 | Nilai kompromi

            1 | Sama penting

            Nilai di sisi kanan slider merupakan reciprocal dari nilai di sisi kiri.
            """)

    # ==========================================================
    # Bangkitkan slider secara dinamis dari config.CRITERIA.
    # Jumlah pasangan akan selalu C(n, 2), dibagi rata ke
    # 2 kolom agar tampilan tetap rapi berapa pun jumlah
    # kriterianya.
    # ==========================================================

    pair_labels = get_pairwise_labels(CRITERIA)

    half = (len(pair_labels) + 1) // 2

    col1, col2 = st.columns(2)

    comparisons = [None] * len(pair_labels)

    with col1:
        for idx in range(0, half):
            first, second = pair_labels[idx]
            label = f"{first} vs {second}"
            comparisons[idx] = pairwise_slider(label, first, second)

    with col2:
        for idx in range(half, len(pair_labels)):
            first, second = pair_labels[idx]
            label = f"{first} vs {second}"
            comparisons[idx] = pairwise_slider(label, first, second)

    if mode == "teknis":

        st.warning(
        """
        ### Tips agar hasil lebih konsisten (CR ≤ 0.10)

        • Berikan penilaian secara logis dan konsisten.

        • Hindari penilaian yang saling bertentangan.

        Contoh:

        Biaya lebih penting daripada Performa.

        Performa lebih penting daripada Keamanan.

        Maka Biaya sebaiknya juga lebih penting daripada Keamanan.

        Semakin konsisten penilaian yang diberikan, semakin kecil nilai Consistency Ratio (CR) yang dihasilkan.

        Apabila nilai CR melebihi 0,10 maka sistem akan melakukan Auto Consistency sebelum menghitung bobot Fuzzy AHP.
        """
        )

    else:

        st.warning(
        """
        ### 💡 Tips agar rekomendasi lebih akurat

        • Berikan penilaian secara logis dan tidak saling bertentangan.

        Contoh:

        Kalau Biaya lebih penting daripada Performa,

        dan Performa lebih penting daripada Keamanan,

        maka sebaiknya Biaya juga lebih penting daripada Keamanan.

        Semakin logis dan konsisten penilaian yang kamu berikan,
        semakin akurat rekomendasi yang dihasilkan sistem untukmu.
        """
        )

    matrix_user = build_pairwise_matrix(comparisons, CRITERIA)

    return matrix_user, CRITERIA