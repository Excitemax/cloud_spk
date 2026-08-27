#input_vizualisation.py
import streamlit as st
import pandas as pd

def show_summary(
    pair_names,
    pair_values
):

    st.header("Visualisasi Preferensi Pengguna")

    st.write("""
    Bagian ini menunjukkan bagaimana
    10 penilaian yang diberikan pengguna
    dibentuk menjadi matriks perbandingan
    berpasangan.
    """)
    
    ####################################################
    # Ringkasan Input
    ####################################################

    st.subheader("1. Ringkasan Input Pengguna")

    ####################################################
    # Mengubah Nilai AHP menjadi Teks
    ####################################################

    pilihan_pengguna = []

    for nama, nilai in zip(pair_names, pair_values):

        kiri = nama.split(" vs ")[0]
        kanan = nama.split(" vs ")[1]

        if nilai == 1:

            teks = "Sama penting"

        elif nilai > 1:

            if nilai == 3:
                teks = f"{kiri} sedikit lebih penting"

            elif nilai == 5:
                teks = f"{kiri} lebih penting"

            elif nilai == 7:
                teks = f"{kiri} sangat lebih penting"

            elif nilai == 9:
                teks = f"{kiri} mutlak lebih penting"

            else:
                teks = f"{kiri} lebih penting"

        else:

            nilai_balik = round(1 / nilai)

            if nilai_balik == 3:
                teks = f"{kanan} sedikit lebih penting"

            elif nilai_balik == 5:
                teks = f"{kanan} lebih penting"

            elif nilai_balik == 7:
                teks = f"{kanan} sangat lebih penting"

            elif nilai_balik == 9:
                teks = f"{kanan} mutlak lebih penting"

            else:
                teks = f"{kanan} lebih penting"

        pilihan_pengguna.append(teks)

    ####################################################
    # Ringkasan Input
    ####################################################

    summary_df = pd.DataFrame({

        "Perbandingan": pair_names,

        "Pilihan Pengguna": pilihan_pengguna,

        "Nilai AHP": [
            round(x, 4)
            for x in pair_values
        ]

    })

    st.dataframe(
        summary_df,
        use_container_width=True
    )

    st.caption("""
    Tabel di atas merupakan seluruh nilai yang
    dimasukkan pengguna melalui dropdown.
    """)
    
def show_interpretation(
    pair_names,
    pair_values
):
    ####################################################
    # Interpretasi Otomatis
    ####################################################

    st.subheader("2. Interpretasi Preferensi")

    interpretasi = []

    for nama, nilai in zip(pair_names, pair_values):

        kiri = nama.split(" vs ")[0]
        kanan = nama.split(" vs ")[1]

        if nilai == 1:

            teks = (
                f"{kiri} sama penting dengan {kanan}."
            )

        elif nilai > 1:

            if nilai == 3:
                tingkat = "sedikit lebih penting"

            elif nilai == 5:
                tingkat = "lebih penting"

            elif nilai == 7:
                tingkat = "sangat lebih penting"

            elif nilai == 9:
                tingkat = "mutlak lebih penting"

            else:
                tingkat = f"{nilai:.2f} kali lebih penting"

            teks = (
                f"{kiri} {tingkat} daripada {kanan}."
            )

        else:

            nilai_balik = round(1 / nilai)

            if nilai_balik == 3:
                tingkat = "sedikit lebih penting"

            elif nilai_balik == 5:
                tingkat = "lebih penting"

            elif nilai_balik == 7:
                tingkat = "sangat lebih penting"

            elif nilai_balik == 9:
                tingkat = "mutlak lebih penting"

            else:
                tingkat = f"{nilai_balik:.2f} kali lebih penting"

            teks = (
                f"{kanan} {tingkat} daripada {kiri}."
            )

        interpretasi.append(teks)

    for item in interpretasi:

        st.write("✅", item)

    st.caption("""
    Interpretasi di atas dibuat secara otomatis
    berdasarkan nilai skala AHP yang dipilih pengguna.
    """)
    
def show_pairwise_matrix(
    matrix_df
):
    ####################################################
    # Matriks Pairwise
    ####################################################

    st.subheader("3. Matriks Pairwise")

    st.dataframe(
        matrix_df,
        use_container_width=True
    )

    st.caption("""
    Matriks di atas merupakan matriks perbandingan
    berpasangan yang akan digunakan pada proses
    Fuzzy AHP.

    Diagonal utama selalu bernilai 1 karena
    setiap kriteria dibandingkan dengan dirinya sendiri.
    """)

def show_heatmap(
    matrix_df
):
    ####################################################
    # Heatmap
    ####################################################

    st.subheader("4. Heatmap Matriks Pairwise")

    styled_matrix = (
        matrix_df.style
        .background_gradient(
            cmap="Blues"
        )
    )

    st.dataframe(
        styled_matrix,
        use_container_width=True
    )

    st.caption("""
    Semakin gelap warna suatu sel,
    semakin besar nilai perbandingan
    antara dua kriteria tersebut.
    """)

def show_status():
    ####################################################
    # Status
    ####################################################

    st.subheader("5. Status Pembentukan Matriks")

    st.success("""
    ✓ Seluruh input berhasil dibentuk menjadi
    matriks pairwise.

    Tahapan berikutnya setelah tombol
    'Hitung Rekomendasi' ditekan adalah:

    1. Uji Konsistensi (Consistency Ratio)

    2. Perhitungan Bobot Fuzzy AHP

    3. Perhitungan TOPSIS

    4. Penentuan Ranking Cloud Computing
    """)
        
def show_input_visualization(
    pair_names,
    pair_values,
    matrix_df
):
    st.divider()

    show_summary(
        pair_names,
        pair_values
    )

    show_interpretation(
        pair_names,
        pair_values
    )

    show_pairwise_matrix(
        matrix_df
    )

    show_heatmap(
        matrix_df
    )

    show_status()   
