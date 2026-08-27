#cloud_data_page.py
import streamlit as st

from modules.cloud_data import get_cloud_data


def show_cloud_data():

    with st.expander(
        "📌 Tahap 5 - Data Penilaian Ahli",
        expanded=False
    ):

        st.header(
            "5. Data Penilaian Alternatif Cloud"
        )

        st.write(
            """
        Setelah bobot setiap kriteria berhasil diperoleh
        menggunakan metode Fuzzy AHP,

        tahap selanjutnya adalah mengambil data
        penilaian alternatif cloud.

        Penilaian alternatif tidak berasal dari pengguna,
        melainkan berasal dari para ahli Cloud Computing.

        Para ahli memberikan penilaian terhadap setiap
        platform cloud berdasarkan lima kriteria yang sama,
        yaitu:

        • Biaya

        • Performa

        • Skalabilitas

        • Keamanan

        • Reliability
        """
        )

        # Mengambil data hasil penilaian para ahli
        cloud_df = get_cloud_data()

        st.caption(
            """
        Data berikut merupakan rata-rata hasil penilaian
        para ahli terhadap masing-masing platform cloud.
        """
        )

        st.dataframe(
            cloud_df.round(4)
        )

        st.info(
            """
        Matriks keputusan ini akan digunakan
        pada proses TOPSIS.
        """
        )

    # ============================================
    # Menyiapkan data yang dibutuhkan oleh
    # metode TOPSIS
    #
    # decision_matrix : matriks keputusan
    # alternatives    : nama alternatif cloud
    # ============================================

    decision_matrix = cloud_df.values

    alternatives = list(
        cloud_df.index
    )

    return (
        cloud_df,
        decision_matrix,
        alternatives
    )