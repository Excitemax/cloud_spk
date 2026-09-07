# ==========================================================
# Cloud Service Recommendation System
# Hybrid Fuzzy AHP - TOPSIS
# ==========================================================
#app.py
# Import Library
import streamlit as st

# Import Halaman Aplikasi
from steps.input_page import show_input
from steps.pairwise_page import show_pairwise
from steps.consistency_page import show_consistency
from steps.final_matrix_page import show_final_matrix
from steps.fuzzy_ahp_page import show_fuzzy_ahp
from steps.cloud_data_page import show_cloud_data
from steps.topsis_page import show_topsis
from steps.ranking_page import show_ranking

# ==========================================================
# Konfigurasi Halaman Streamlit
# ==========================================================

st.set_page_config(
    page_title="Cloud Service Recommendation",
    page_icon="☁️",
    layout="wide"
)

# ==========================================================
# CSS Ringkas
#
# Streamlit secara default memberi padding/margin cukup besar
# di atas judul dan di sekitar heading/divider, sehingga
# tampilan awal terasa "lapang" dan tidak muat dalam satu
# screenshot. Blok CSS ini memperkecil jarak-jarak tersebut
# tanpa mengubah konten/logika aplikasi sama sekali.
# ==========================================================

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 1rem;
        }
        h1 {
            margin-bottom: 0rem;
            padding-bottom: 0rem;
        }
        h3 {
            margin-top: 0rem;
            padding-top: 0rem;
        }
        hr {
            margin: 0.6rem 0;
        }
        div[data-testid="stMarkdownContainer"] p {
            margin-bottom: 0.3rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Header Aplikasi

st.title("☁️ Cloud Service Recommendation System")

st.subheader("Hybrid Fuzzy AHP - TOPSIS")

st.markdown("""
Sistem pendukung keputusan ini membantu pengguna memilih
platform **Cloud Computing** yang paling sesuai berdasarkan
preferensi terhadap lima kriteria utama menggunakan metode
**Hybrid Fuzzy AHP - TOPSIS**.
""")

st.divider()
# ==========================================================
# Tahapan Sistem Rekomendasi
#
# 1. Pengguna memberikan preferensi antar kriteria
# 2. Sistem membentuk matriks perbandingan AHP
# 3. Sistem menguji konsistensi matriks
# 4. Jika matriks tidak konsisten, sistem melakukan
#    perbaikan otomatis
# 5. Sistem menghitung bobot menggunakan Fuzzy AHP
# 6. Sistem mengambil data penilaian ahli
# 7. Sistem melakukan perangkingan menggunakan TOPSIS
# 8. Sistem menampilkan rekomendasi cloud terbaik
# ==========================================================

# ==========================================================
# Tahap Awal
#
# Menampilkan halaman input preferensi pengguna.
#
# Fungsi ini menghasilkan:
# - matrix_user : matriks perbandingan berpasangan AHP
# - criteria    : daftar nama kriteria
# ==========================================================

matrix_user, criteria = show_input()

# ==========================================================
# Proses Perhitungan
#
# Seluruh proses hanya dijalankan ketika pengguna
# menekan tombol "Hitung Rekomendasi".
#
# CATATAN PERBAIKAN:
# Pada versi sebelumnya, blok "with st.spinner(...)" hanya
# membungkus Tahap 1 (show_pairwise), sehingga indikator
# loading hilang lebih cepat daripada proses perhitungan
# yang sebenarnya (Tahap 2-7 berjalan tanpa spinner). Pada
# versi ini, seluruh tahap perhitungan telah disejajarkan
# agar berada di dalam satu blok spinner yang sama.
# ==========================================================

if st.button(
    "🚀 Hitung Rekomendasi",
    use_container_width=True
):
    try:
        with st.spinner(
            "Sedang menghitung rekomendasi..."
        ):

            # ==================================================
            # Tahap 1
            # Menampilkan matriks perbandingan berpasangan
            # (Pairwise) yang dibentuk dari input pengguna.
            # ==================================================

            show_pairwise(
                matrix_user,
                criteria
            )

            # ==================================================
            # Tahap 2
            #
            # Menguji konsistensi matriks menggunakan metode AHP.
            #
            # Output:
            # active_matrix      -> matriks yang akan digunakan
            # consistency_result -> hasil pengujian konsistensi
            #
            # Jika matriks tidak konsisten maka sistem akan
            # memperbaiki matriks secara otomatis.
            # ==================================================

            active_matrix, consistency_result = show_consistency(
                matrix_user,
                criteria
            )

            # ==================================================
            # Tahap 3
            #
            # Menampilkan matriks akhir yang digunakan pada
            # proses Fuzzy AHP serta menghitung bobot setiap
            # kriteria.
            #
            # Output:
            # fuzzy_result -> seluruh hasil perhitungan Fuzzy AHP
            # weights      -> bobot akhir setiap kriteria
            # ==================================================

            fuzzy_result, weights = show_final_matrix(
                active_matrix,
                criteria,
                consistency_result
            )

            # ==================================================
            # Tahap 4
            #
            # Menampilkan seluruh proses perhitungan Fuzzy AHP,
            # meliputi:
            # - Synthetic Extent
            # - Defuzzification
            # - Bobot akhir kriteria
            # ==================================================

            show_fuzzy_ahp(
                fuzzy_result,
                weights,
                criteria
            )

            # ==================================================
            # Tahap 5
            # Mengambil matriks keputusan hasil penilaian ahli.
            # ==================================================

            cloud_df, decision_matrix, alternatives = show_cloud_data()

            # ==================================================
            # Tahap 6
            #
            # Menghitung perangkingan alternatif menggunakan
            # metode TOPSIS berdasarkan:
            #
            # - bobot hasil Fuzzy AHP
            # - data penilaian para ahli
            #
            # Output:
            # topsis_result -> seluruh hasil perhitungan TOPSIS
            # ==================================================

            topsis_result = show_topsis(
                decision_matrix,
                weights,
                alternatives,
                criteria
            )

            # ==================================================
            # Tahap 7
            #
            # Menampilkan hasil akhir berupa:
            # - ranking seluruh alternatif
            # - nilai preferensi
            # - rekomendasi platform cloud terbaik
            # ==================================================

            show_ranking(
                topsis_result
            )

    except Exception as e:
        st.error(
            "Terjadi kendala saat memproses perhitungan. "
            "Silakan periksa kembali preferensi yang dimasukkan "
            "lalu coba tekan tombol Hitung Rekomendasi kembali.\n\n"
            f"Detail teknis: {e}"
        )