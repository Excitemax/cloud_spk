#consistency_page.py
import streamlit as st
import pandas as pd

from modules.consistency import consistency_test
from modules.inconsistency_analyzer import find_inconsistent_pairs
from modules.auto_consistency import auto_fix_matrix


def show_consistency(
    matrix_user,
    criteria
):

    consistency_result = consistency_test(
            matrix_user
        )

    with st.expander(
            "📌 Tahap 2 - Uji Konsistensi",
            expanded=False
        ):
            st.header("2. Uji Konsistensi")
            st.caption(
                "Tahap ini bertujuan untuk memastikan bahwa "
                "penilaian pengguna bersifat logis dan konsisten."
            )
            
            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Lambda Max",
                round(
                    consistency_result["lambda_max"],
                    4
                )
            )

            col2.metric(
                "CI",
                round(
                    consistency_result["ci"],
                    4
                )
            )

            col3.metric(
                "CR",
                round(
                    consistency_result["cr"],
                    4
                )
            )

            st.info(
                """
            Interpretasi Consistency Ratio (CR)

            ✓ CR < 0.10
            Matriks dinyatakan konsisten.

            ✗ CR ≥ 0.10
            Matriks perlu diperbaiki.
            """
            )
            
            active_matrix = matrix_user
            
        # ----------------------------------------------------------
        # Pemeriksaan Konsistensi
        #
        # Jika CR lebih dari 0.10 maka sistem akan
        # melakukan perbaikan otomatis menggunakan
        # metode eigenvector.
        # ----------------------------------------------------------

            if not consistency_result["is_consistent"]:

                st.warning(
                    f"""
                Matriks tidak memenuhi syarat konsistensi.

                Consistency Ratio (CR) = {consistency_result['cr']:.4f}

                Sistem akan melakukan proses perbaikan otomatis
                agar bobot yang dihasilkan lebih valid.
                """
                )

                issues = find_inconsistent_pairs(
                    matrix_user,
                    criteria
                )

                st.subheader(
                    "Pasangan Perbandingan Dengan Error Terbesar"
                )

                st.caption(
                    """
                Semakin besar nilai error, semakin besar kontribusi
                pasangan tersebut terhadap ketidakkonsistenan matriks.
                """
                )

                st.dataframe(
                    pd.DataFrame(issues[:5])
                )
                
                st.subheader(
                    "Saran Perbaikan Penilaian"
                )

                st.write(
                    """
                Berikut adalah pasangan kriteria yang paling
                berkontribusi terhadap ketidakkonsistenan.

                Sistem menyarankan agar pengguna meninjau
                kembali penilaian berikut.
                """
                )
                
                skala_saaty = [1, 2, 3, 4, 5, 6, 7, 8, 9]

                for item in issues[:5]:

                    pair = item["pair"]
                    actual = item["actual"]
                    expected = item["expected"]
                    error = item["error"]

                    kiri, kanan = pair.split(" vs ")

                    # Bulatkan nilai rekomendasi ke skala Saaty terdekat

                    rekomendasi = min(
                        skala_saaty,
                        key=lambda x: abs(x - expected)
                    )

                    if actual > rekomendasi:

                        saran = (
                            f"Kurangi tingkat kepentingan **{kiri}** terhadap **{kanan}**."
                        )

                    elif actual < rekomendasi:

                        saran = (
                            f"Tingkatkan tingkat kepentingan **{kiri}** terhadap **{kanan}**."
                        )

                    else:

                        saran = (
                            "Nilai sudah mendekati nilai ideal."
                        )

                    st.warning(
                        f"""
                ### ⚠️ Perbandingan yang Perlu Ditinjau

                **{pair}**

                **Nilai saat ini :** {actual}

                **Nilai ideal hasil analisis :** {expected:.2f}

                **Nilai yang disarankan (Skala Saaty) :** {rekomendasi}

                **Kontribusi terhadap inkonsistensi :** {error:.4f}

                **Saran Sistem :**

                {saran}
                """
                    )
                
                fixed_matrix, _ = (
                        auto_fix_matrix(matrix_user)
                    )
                
                active_matrix = fixed_matrix
                
                fixed_consistency = consistency_test(
                    fixed_matrix
                )
                
                cr_baru = max(
                fixed_consistency["cr"],
                    0
                )
                
                st.success(
                    f"""
                Perbaikan matriks berhasil dilakukan.

                Consistency Ratio setelah perbaikan
                = {cr_baru:.4f}
                """
                )
                
                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "CR Sebelum",
                        round(
                            consistency_result["cr"],
                            4
                        )
                    )

                with col2:
                    st.metric(
                        "CR Sesudah",
                        round(
                            cr_baru,
                            4
                        )
                    )
                
                st.info(
                    "Perbaikan dilakukan menggunakan "
                    "metode eigenvector untuk menghasilkan "
                    "matriks yang memenuhi syarat konsistensi "
                    "(CR < 0.1)."
                )

                st.subheader(
                    "Matriks Konsisten Hasil Perbaikan"
                )
                st.caption(
                    "Matriks berikut digunakan pada proses "
                    "perhitungan Fuzzy AHP."
                )

                st.dataframe(
                    pd.DataFrame(
                        fixed_matrix,
                        index=criteria,
                        columns=criteria
                    ).round(4)
                )
            else:
                st.success(
                    """
                Matriks telah memenuhi syarat konsistensi.

                Perhitungan Fuzzy AHP akan menggunakan
                matriks asli dari pengguna.
                """
                )
            return active_matrix, consistency_result