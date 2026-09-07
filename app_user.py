# ==========================================================
# Cloud Service Recommendation System
# Hybrid Fuzzy AHP - TOPSIS
# VERSI PENGGUNA (langsung ke hasil akhir)
# ==========================================================
# app_user.py
#
# Beda dengan app.py (versi sidang/demo teknis yang
# menampilkan setiap tahap perhitungan), file ini adalah
# versi yang ditujukan untuk pengguna akhir/awam:
#
#   1. Pengguna mengisi slider preferensi antar kriteria.
#   2. Pengguna menekan tombol "Hitung Rekomendasi".
#   3. Sistem langsung menampilkan hasil akhir berupa
#      platform cloud yang direkomendasikan, beserta
#      alasan dalam bahasa yang mudah dipahami.
#
# Tidak ada istilah teknis (matriks, TFN, eigenvector,
# Consistency Ratio, dsb.) yang ditampilkan ke pengguna.
# Seluruh perbaikan konsistensi tetap dilakukan otomatis
# di balik layar.
# ==========================================================

import streamlit as st
import numpy as np
import pandas as pd

from pages.input_page import show_input

from modules.consistency import consistency_test
from modules.auto_consistency import auto_fix_matrix
from modules.fuzzy_ahp import calculate_fuzzy_ahp
from modules.cloud_data import get_cloud_data
from modules.topsis import calculate_topsis


# ==========================================================
# Konfigurasi Halaman
# ==========================================================

st.set_page_config(
    page_title="Rekomendasi Cloud Terbaik",
    page_icon="☁️",
    layout="centered"
)

# ==========================================================
# CSS Ringkas - lihat penjelasan di app.py.
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

st.title("☁️ Cari Platform Cloud Terbaik untuk Anda")

st.markdown(
    """
Geser slider di bawah untuk menunjukkan mana yang lebih
penting bagi Anda di antara dua kriteria, lalu tekan tombol
**Hitung Rekomendasi** untuk mendapatkan rekomendasi
platform *cloud computing* yang paling sesuai.
"""
)

st.divider()


# ==========================================================
# Fungsi bantu: menyusun alasan rekomendasi dalam
# bahasa yang mudah dipahami pengguna awam.
# ==========================================================

def _format_persen(x):
    return f"{x * 100:.0f}%"


def build_reasoning(criteria, weights, cloud_df, ranking):
    """
    Menyusun penjelasan naratif mengapa platform tertentu
    direkomendasikan, berdasarkan:

    1. Kriteria mana yang paling penting menurut preferensi
       pengguna (bobot Fuzzy AHP terbesar).
    2. Bagaimana performa platform pemenang pada kriteria-
       kriteria tersebut dibandingkan platform lain.
    """

    best_platform, best_score = ranking[0]

    # Urutkan kriteria dari yang paling penting menurut
    # preferensi pengguna.
    weight_pairs = list(zip(criteria, weights))
    weight_pairs.sort(key=lambda x: x[1], reverse=True)

    top_criteria = [name for name, _ in weight_pairs[:2]]

    alasan = []

    for kriteria_nama in top_criteria:

        nilai_platform = cloud_df.loc[best_platform, kriteria_nama]
        rata_rata_lain = cloud_df.drop(index=best_platform)[kriteria_nama].mean()

        if nilai_platform >= rata_rata_lain:
            posisi = "lebih unggul dibandingkan rata-rata platform lain"
        else:
            posisi = "sedikit di bawah rata-rata platform lain, namun tetap kompetitif"

        alasan.append(
            f"- Pada kriteria **{kriteria_nama}** (salah satu prioritas "
            f"utama Anda), **{best_platform}** {posisi} "
            f"(skor {nilai_platform:.2f} dari skala penilaian ahli)."
        )

    return best_platform, best_score, top_criteria, alasan


# ==========================================================
# Tahap Input
# ==========================================================

matrix_user, criteria = show_input()

hitung = st.button(
    "🚀 Hitung Rekomendasi",
    use_container_width=True
)

if hitung:

    with st.spinner("Sedang menghitung rekomendasi terbaik untuk Anda..."):

        try:
            # --------------------------------------------------
            # Uji konsistensi & perbaikan otomatis (diam-diam).
            #
            # Jika preferensi yang dimasukkan pengguna tidak
            # konsisten secara logis, sistem memperbaikinya
            # sendiri tanpa meminta pengguna mengubah slider,
            # dan tanpa menampilkan istilah teknis apa pun.
            # --------------------------------------------------

            consistency_result = consistency_test(matrix_user)

            if consistency_result["is_consistent"]:
                active_matrix = matrix_user
            else:
                active_matrix, _ = auto_fix_matrix(matrix_user)

            # --------------------------------------------------
            # Bobot kriteria (Fuzzy AHP)
            # --------------------------------------------------

            fuzzy_result = calculate_fuzzy_ahp(active_matrix)
            weights = fuzzy_result["final_weights"]

            # --------------------------------------------------
            # Data penilaian ahli & perangkingan (TOPSIS)
            # --------------------------------------------------

            cloud_df = get_cloud_data()
            decision_matrix = cloud_df.values
            alternatives = list(cloud_df.index)

            topsis_result = calculate_topsis(
                decision_matrix,
                np.array(weights),
                alternatives
            )

            ranking = topsis_result["ranking"]

        except Exception as e:
            st.error(
                "Terjadi kendala saat menghitung rekomendasi. "
                "Silakan periksa kembali preferensi Anda dan coba lagi.\n\n"
                f"Detail teknis: {e}"
            )
            st.stop()

    # ======================================================
    # Hasil Akhir
    # ======================================================

    best_platform, best_score, top_criteria, alasan = build_reasoning(
        criteria,
        weights,
        cloud_df,
        ranking
    )

    st.divider()

    st.success(
        f"### ✅ Rekomendasi untuk Anda: **{best_platform}**"
    )

    st.markdown(
        f"""
Berdasarkan preferensi yang Anda masukkan, **{best_platform}**
adalah platform *cloud computing* yang paling sesuai, dengan
tingkat kecocokan **{_format_persen(best_score)}** dari skor
maksimal.
"""
    )

    st.subheader("Kenapa platform ini yang direkomendasikan?")

    st.markdown(
        f"""
Dari kelima kriteria yang ada, dua yang paling Anda
prioritaskan adalah **{top_criteria[0]}** dan
**{top_criteria[1]}**. Berikut alasan {best_platform}
unggul untuk Anda:
"""
    )

    for baris in alasan:
        st.markdown(baris)

    st.divider()

    st.subheader("Perbandingan Seluruh Platform")

    ranking_df = pd.DataFrame(
        ranking,
        columns=["Platform", "Tingkat Kecocokan"]
    )

    ranking_df.index = ranking_df.index + 1
    ranking_df.index.name = "Peringkat"

    ranking_df["Tingkat Kecocokan"] = ranking_df[
        "Tingkat Kecocokan"
    ].apply(_format_persen)

    st.dataframe(
        ranking_df,
        use_container_width=True
    )

    st.caption(
        "Tingkat kecocokan dihitung berdasarkan seberapa dekat "
        "setiap platform dengan kondisi paling ideal menurut "
        "kombinasi preferensi Anda dan penilaian para ahli "
        "*cloud computing* terhadap kelima kriteria di atas."
    )