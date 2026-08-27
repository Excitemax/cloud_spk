#ranking_page.py
import streamlit as st
import pandas as pd


def show_ranking(
    topsis_result
):

    with st.expander(
        "📌 Tahap 7 - Ranking dan Rekomendasi",
        expanded=True
    ):

        st.header(
            "Ranking Cloud Service"
        )

        ranking_df = pd.DataFrame(
            topsis_result["ranking"],
            columns=[
                "Platform",
                "Nilai Preferensi"
            ]
        )

        ranking_df.index = (
            ranking_df.index + 1
        )

        ranking_df[
            "Nilai Preferensi"
        ] = (
            ranking_df[
                "Nilai Preferensi"
            ].round(4)
        )

        st.dataframe(
            ranking_df,
            use_container_width=True
        )

        ##################################################
        # Cloud Terbaik
        ##################################################

        best_cloud = (
            topsis_result["ranking"][0][0]
        )

        best_score = (
            topsis_result["ranking"][0][1]
        )

        st.success(
            f"""
Rekomendasi Cloud Terbaik:

**{best_cloud}**
"""
        )

        st.info(
            f"""
{best_cloud} memperoleh nilai preferensi
tertinggi sebesar **{best_score:.4f}**.

Berdasarkan kombinasi bobot Fuzzy AHP
dan perhitungan TOPSIS,
platform tersebut menjadi alternatif
cloud yang paling optimal sesuai
dengan preferensi pengguna.
"""
        )