#topsis_page.py
import streamlit as st
import pandas as pd
import numpy as np

from modules.topsis import calculate_topsis


def show_topsis(
    decision_matrix,
    weights,
    alternatives,
    criteria
):

    topsis_result = calculate_topsis(
        decision_matrix,
        np.array(weights),
        alternatives
    )

    with st.expander(
        "📌 Tahap 6 - Perhitungan TOPSIS",
        expanded=False
    ):

        ###################################################
        # Normalisasi
        ###################################################

        st.subheader("6.1 Normalisasi")

        normalized_df = pd.DataFrame(
            topsis_result["normalized_matrix"],
            index=alternatives,
            columns=criteria
        ).round(4)

        st.dataframe(normalized_df)

        st.caption(
            """
        Normalisasi dilakukan agar seluruh
        kriteria berada pada skala yang sama
        sebelum diberikan bobot.
        """
        )

        ###################################################
        # Matriks Terbobot
        ###################################################

        st.subheader("6.2 Matriks Terbobot")

        weighted_df = pd.DataFrame(
            topsis_result["weighted_matrix"],
            index=alternatives,
            columns=criteria
        ).round(4)

        st.dataframe(weighted_df)

        st.caption(
            """
        Nilai pada matriks ini diperoleh
        dari hasil perkalian matriks
        normalisasi dengan bobot
        Fuzzy AHP.
        """
        )

        ###################################################
        # Solusi Ideal
        ###################################################

        st.subheader("6.3 Solusi Ideal")

        ideal_df = pd.DataFrame(
            {
                "A+":
                    topsis_result["ideal_positive"],

                "A-":
                    topsis_result["ideal_negative"]

            },
            index=criteria
        ).round(4)

        st.dataframe(ideal_df)

        st.caption(
            """
        A+ merupakan solusi ideal positif.

        A− merupakan solusi ideal negatif.
        """
        )

        ###################################################
        # Jarak
        ###################################################

        st.header(
            "Jarak Terhadap Solusi Ideal"
        )

        distance_df = pd.DataFrame(
            {
                "Alternatif":
                    alternatives,

                "D+":
                    topsis_result["d_positive"],

                "D-":
                    topsis_result["d_negative"]
            }
        ).round(4)

        st.dataframe(distance_df)

        st.caption(
            """
        Semakin kecil D+
        dan semakin besar D−,
        maka alternatif semakin baik.
        """
        )

        ###################################################
        # Preferensi
        ###################################################

        st.header(
            "Nilai Preferensi TOPSIS"
        )

        preference_df = pd.DataFrame(
            {
                "Platform":
                    alternatives,

                "Nilai Preferensi":
                    topsis_result["preference"]
            }
        )

        preference_df[
            "Nilai Preferensi"
        ] = (
            preference_df[
                "Nilai Preferensi"
            ].round(4)
        )

        preference_df = preference_df.sort_values(
            by="Nilai Preferensi",
            ascending=False
        )

        st.dataframe(preference_df)

        st.bar_chart(
            preference_df.set_index(
                "Platform"
            )
        )

        st.caption(
            """
        Alternatif dengan nilai preferensi
        terbesar merupakan platform cloud
        yang paling direkomendasikan.
        """
        )

    return topsis_result