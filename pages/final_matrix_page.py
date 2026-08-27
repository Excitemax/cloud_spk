#final_matrix_page.py

import streamlit as st
import pandas as pd
from modules.fuzzy_ahp import calculate_fuzzy_ahp

def show_final_matrix(
    active_matrix,
    criteria,
    consistency_result
):
    with st.expander(
        "📌 Tahap 3 - Matriks Akhir",
        expanded=False
    ):
        st.header(
            "3. Matriks Akhir Yang Digunakan"
        )

        st.caption(
            """
        Matriks berikut merupakan matriks yang digunakan
        pada proses perhitungan bobot menggunakan
        Fuzzy AHP.
        """
        )
        
        st.dataframe(
            pd.DataFrame(
                active_matrix,
                index=criteria,
                columns=criteria
            ).round(4)
        )
            
        if not consistency_result["is_consistent"]:
            st.info(
                "Karena nilai CR melebihi batas "
                "0.1, bobot Fuzzy AHP dihitung "
                "menggunakan matriks hasil "
                "perbaikan untuk menjamin "
                "konsistensi penilaian."
            )
        
        fuzzy_result = calculate_fuzzy_ahp(
            active_matrix
        )

        weights = fuzzy_result[
            "final_weights"
        ]
        
        return (
            fuzzy_result,
            weights
        )