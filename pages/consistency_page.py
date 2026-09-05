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

    with st.expander(
        "📌 Tahap 2 - Uji Konsistensi",
        expanded=False
    ):
        st.header("2. Uji Konsistensi")
        st.caption(
            "Tahap ini bertujuan untuk memastikan bahwa "
            "penilaian pengguna bersifat logis dan konsisten."
        )

        # ------------------------------------------------------
        # Seluruh perhitungan dibungkus try/except agar apabila
        # terjadi kesalahan input atau numerik yang tidak
        # terduga, pengguna melihat pesan yang jelas alih-alih
        # aplikasi berhenti tiba-tiba (crash).
        # ------------------------------------------------------

        try:
            consistency_result = consistency_test(
                matrix_user
            )
        except ValueError as e:
            st.error(
                f"Matriks perbandingan tidak dapat diproses: {e}"
            )
            st.stop()

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
        # Jika CR >= 0.10, sistem TIDAK menyarankan nilai
        # pengganti untuk penilaian pengguna/ahli. Sistem hanya
        # menampilkan dua hal yang bersifat informatif:
        #
        # 1. Ranking pasangan kriteria yang paling berkontribusi
        #    terhadap ketidakkonsistenan.
        # 2. Ranking prioritas kriteria versi konsisten, sebagai
        #    hasil sampingan dari proses perbaikan otomatis.
        #
        # Perbaikan matriks selalu dilakukan secara otomatis
        # menggunakan metode eigenvector (auto_fix_matrix), yang
        # menjamin CR hasil perbaikan = 0 (transitif sempurna),
        # tanpa memerlukan input tambahan dari pengguna/ahli.
        # ----------------------------------------------------------

        if not consistency_result["is_consistent"]:

            st.warning(
                f"""
            Matriks tidak memenuhi syarat konsistensi.

            Consistency Ratio (CR) = {consistency_result['cr']:.4f}

            Sistem akan melakukan perbaikan otomatis terhadap
            matriks menggunakan metode eigenvector, sehingga
            proses Fuzzy AHP tetap dapat dilanjutkan dengan
            matriks yang konsisten.
            """
            )

            # ------------------------------------------------------
            # 1. Ranking kontribusi ketidakkonsistenan
            # ------------------------------------------------------

            try:
                issues = find_inconsistent_pairs(
                    matrix_user,
                    criteria
                )
            except Exception as e:
                issues = []
                st.error(
                    f"Analisis kontribusi ketidakkonsistenan "
                    f"gagal dijalankan: {e}"
                )

            if issues:

                st.subheader(
                    "Pasangan Perbandingan Paling Berkontribusi "
                    "Terhadap Ketidakkonsistenan"
                )

                st.caption(
                    """
                Daftar berikut diurutkan dari kontribusi terbesar
                ke terkecil terhadap nilai Consistency Ratio (CR).
                Daftar ini bersifat informatif untuk membantu
                memahami sumber ketidakkonsistenan, dan bukan
                merupakan instruksi untuk mengubah nilai slider
                tertentu.
                """
                )

                issues_df = pd.DataFrame(issues).rename(columns={
                    "pair": "Pasangan Kriteria",
                    "actual": "Nilai Slider Pengguna",
                    "expected": "Nilai Ideal (Analitis)",
                    "error": "Kontribusi Terhadap Inkonsistensi",
                })
                issues_df.index = issues_df.index + 1
                issues_df.index.name = "Peringkat"

                st.dataframe(
                    issues_df.round(4),
                    use_container_width=True
                )

            # ------------------------------------------------------
            # Perbaikan otomatis (selalu dijalankan)
            # ------------------------------------------------------

            try:
                fixed_matrix, weights = auto_fix_matrix(
                    matrix_user
                )

                fixed_consistency = consistency_test(
                    fixed_matrix
                )

            except ValueError as e:
                st.error(
                    f"Perbaikan matriks otomatis gagal dilakukan: {e}"
                )
                st.stop()

            active_matrix = fixed_matrix

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
                "Perbaikan dilakukan menggunakan metode "
                "eigenvector, yaitu merekonstruksi matriks "
                "perbandingan berpasangan dari satu vektor "
                "bobot tunggal (aij = wi / wj). Matriks yang "
                "dibentuk dengan cara ini bersifat transitif "
                "sempurna, sehingga CR hasil perbaikan akan "
                "selalu bernilai 0, berapa pun input awal yang "
                "diberikan pengguna."
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

            # ------------------------------------------------------
            # 2. Ranking prioritas kriteria (versi konsisten)
            # ------------------------------------------------------

            st.subheader(
                "Prioritas Kriteria Hasil Perbaikan"
            )

            st.caption(
                """
            Bobot berikut diturunkan dari eigenvector yang
            sama dengan yang digunakan untuk membentuk matriks
            konsisten di atas, dan menggambarkan urutan
            kepentingan kriteria dari yang paling penting
            hingga yang paling tidak penting.
            """
            )

            priority_df = pd.DataFrame({
                "Kriteria": criteria,
                "Bobot (Eigenvector)": weights
            }).sort_values(
                by="Bobot (Eigenvector)",
                ascending=False
            ).reset_index(drop=True)

            priority_df.index = priority_df.index + 1
            priority_df.index.name = "Peringkat"

            st.dataframe(
                priority_df.round(4),
                use_container_width=True
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