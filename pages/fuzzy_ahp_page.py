#fuzzy_ahp_page.py
import streamlit as st
import pandas as pd
import numpy as np

def show_fuzzy_ahp(
    fuzzy_result,
    weights,
    criteria
):
    with st.expander(
        "📌 Tahap 4 - Fuzzy AHP",
        expanded=False
    ):
        st.header("4. Perhitungan Bobot Kriteria Menggunakan Fuzzy AHP")
        
        st.caption(
            """
        Tahapan ini mengubah matriks AHP menjadi TFN
        dan menghasilkan bobot kriteria.
        """
        )
        
        st.subheader("4.1 Nilai Synthetic Extent")

        st.caption(
            """
        Tabel berikut menunjukkan nilai
        L, M, dan U setiap kriteria.
        """
        )
        
        synthetic_df = pd.DataFrame(
            fuzzy_result["synthetic_extent"],
            columns=["L", "M", "U"],
            index=criteria
        )

        st.dataframe(synthetic_df)
        
        st.info(
            """
        L = Lower Value

        M = Middle Value

        U = Upper Value
        """
        )
    
        st.subheader("4.2 Defuzzification")

        st.caption(
            """
        Nilai fuzzy kemudian diubah menjadi nilai crisp
        menggunakan metode Center of Area (COA).
        """
        )

        crisp_df = pd.DataFrame({
            "Kriteria": criteria,
            "Crisp Value":
                fuzzy_result["crisp_weights"]
        })

        st.dataframe(crisp_df)

        st.info(
            """
        Semakin besar nilai crisp,
        semakin besar tingkat kepentingan suatu kriteria.
        """
        )
        
    # ----------------------------------------------------------
    # Normalisasi Bobot
    #
    # Nilai crisp dinormalisasi sehingga total bobot = 1
    # ----------------------------------------------------------

        weight_df = pd.DataFrame({
            "Kriteria": criteria,
            "Bobot": [
                round(w, 4)
                for w in weights
            ],
            "Persentase": [
                f"{w*100:.2f}%"
                for w in weights
            ]
        })

        st.subheader("4.3 Bobot Akhir Kriteria")

        st.caption(
            """
        Bobot berikut merupakan hasil akhir metode
        Fuzzy AHP dan akan digunakan pada proses
        perankingan TOPSIS.
        """
        )

        st.dataframe(weight_df)
        
        max_weight = max(weights)

        max_index = np.argmax(weights)

        st.success(
            f"""
        Kriteria dengan bobot terbesar adalah

        **{criteria[max_index]}**

        dengan bobot **{max_weight:.4f}**
        """
        )
        
        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Bobot Terbesar",
                f"{max_weight:.4f}"
            )

        with col2:
            st.metric(
                "Total Bobot",
                f"{round(sum(weights), 4)}"
            )

        st.caption(
            """
        Jumlah seluruh bobot harus bernilai 1
        karena telah melalui proses normalisasi.
        """
        )