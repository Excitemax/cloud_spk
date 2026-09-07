#pairwise_page.py
import streamlit as st
import pandas as pd

def show_pairwise(matrix_user, criteria):

    with st.expander(
            "📌 Tahap 1 - Matriks Perbandingan Kriteria",
            expanded=True
        ):
            st.header("1. Matriks Perbandingan Kriteria")
            st.caption(
                "Matriks berikut dibentuk berdasarkan preferensi "
                "pengguna menggunakan metode AHP."
            )

            df_matrix = pd.DataFrame(
                matrix_user,
                index=criteria,
                columns=criteria
            ).round(4)

            st.dataframe(df_matrix)