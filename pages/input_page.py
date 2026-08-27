#input_page.py
import streamlit as st
import numpy as np

# ==========================================================
# Fungsi untuk membuat pilihan pairwise
# ==========================================================

def pairwise_slider(label, first, second):

    st.markdown(f"**{label}**")

    st.markdown(
        f"""
        <div style="display:flex;
                    justify-content:space-between;
                    font-weight:bold;
                    margin-bottom:5px;">
            <span>{first}</span>
            <span>{second}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style='display:flex;
                    justify-content:space-between;
                    font-size:12px;'>
            <span>9</span><span>8</span><span>7</span><span>6</span>
            <span>5</span><span>4</span><span>3</span><span>2</span>
            <span>1</span>
            <span>2</span><span>3</span><span>4</span><span>5</span>
            <span>6</span><span>7</span><span>8</span><span>9</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style='display:flex;
                    justify-content:space-between;
                    font-size:11px;
                    color:gray;
                    margin-bottom:5px;'>
            <span>← {first} lebih penting</span>
            <span>{second} lebih penting →</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    position = st.slider(
        "",
        min_value=-8,
        max_value=8,
        value=0,
        step=1,
        label_visibility="collapsed",
        key=label
    )
    
    display = {
    -8: f"{first} mutlak lebih penting",
    -7: f"{first} berada di antara sangat dan mutlak lebih penting",
    -6: f"{first} sangat lebih penting",
    -5: f"{first} berada di antara lebih penting dan sangat lebih penting",
    -4: f"{first} lebih penting",
    -3: f"{first} berada di antara sedikit dan lebih penting",
    -2: f"{first} sedikit lebih penting",
    -1: f"{first} berada di antara sama dan sedikit lebih penting",

    0: "Kedua kriteria sama penting",

    1: f"{second} berada di antara sama dan sedikit lebih penting",
    2: f"{second} sedikit lebih penting",
    3: f"{second} berada di antara sedikit dan lebih penting",
    4: f"{second} lebih penting",
    5: f"{second} berada di antara lebih penting dan sangat lebih penting",
    6: f"{second} sangat lebih penting",
    7: f"{second} berada di antara sangat dan mutlak lebih penting",
    8: f"{second} mutlak lebih penting"
    }

    st.caption(display[position])

    mapping = {
        -8: 9,
        -7: 8,
        -6: 7,
        -5: 6,
        -4: 5,
        -3: 4,
        -2: 3,
        -1: 2,
         0: 1,
         1: 1/2,
         2: 1/3,
         3: 1/4,
         4: 1/5,
         5: 1/6,
         6: 1/7,
         7: 1/8,
         8: 1/9
    }

    return mapping[position]

def show_input():

    st.header("Input Preferensi Kriteria")

    st.info("""
    Geser slider untuk menentukan tingkat kepentingan antar dua kriteria.

    • Geser ke kiri apabila kriteria di sebelah kiri lebih diprioritaskan.

    • Geser ke kanan apabila kriteria di sebelah kanan lebih diprioritaskan.

    • Posisi tengah menunjukkan kedua kriteria memiliki tingkat kepentingan yang sama.
    """)

    with st.expander("Lihat Konversi Pilihan ke Nilai AHP"):

        st.markdown("""
        Nilai AHP | Makna

        9 | Mutlak lebih penting

        8 | Nilai kompromi

        7 | Sangat lebih penting

        6 | Nilai kompromi

        5 | Lebih penting

        4 | Nilai kompromi

        3 | Sedikit lebih penting

        2 | Nilai kompromi

        1 | Sama penting
        
        Nilai di sisi kanan slider merupakan reciprocal dari nilai di sisi kiri.
        """)

    # ==========================================================
    # Input Pairwise Comparison
    # ==========================================================
    col1, col2 = st.columns(2)

    with col1:

        b_p = pairwise_slider(
            "Biaya vs Performa",
            "Biaya",
            "Performa"
        )

        b_s = pairwise_slider(
            "Biaya vs Skalabilitas",
            "Biaya",
            "Skalabilitas"
        )

        b_k = pairwise_slider(
            "Biaya vs Keamanan",
            "Biaya",
            "Keamanan"
        )

        b_r = pairwise_slider(
            "Biaya vs Reliability",
            "Biaya",
            "Reliability"
        )

        p_s = pairwise_slider(
            "Performa vs Skalabilitas",
            "Performa",
            "Skalabilitas"
        )


    with col2:

        p_k = pairwise_slider(
            "Performa vs Keamanan",
            "Performa",
            "Keamanan"
        )

        p_r = pairwise_slider(
            "Performa vs Reliability",
            "Performa",
            "Reliability"
        )

        s_k = pairwise_slider(
            "Skalabilitas vs Keamanan",
            "Skalabilitas",
            "Keamanan"
        )

        s_r = pairwise_slider(
            "Skalabilitas vs Reliability",
            "Skalabilitas",
            "Reliability"
        )

        k_r = pairwise_slider(
            "Keamanan vs Reliability",
            "Keamanan",
            "Reliability"
        )


    st.warning(
    """
    ### Tips agar hasil lebih konsisten (CR ≤ 0.10)

    • Berikan penilaian secara logis dan konsisten.

    • Hindari penilaian yang saling bertentangan.

    Contoh:

    Biaya lebih penting daripada Performa.

    Performa lebih penting daripada Keamanan.

    Maka Biaya sebaiknya juga lebih penting daripada Keamanan.

    Semakin konsisten penilaian yang diberikan, semakin kecil nilai Consistency Ratio (CR) yang dihasilkan.
    
    Apabila nilai CR melebihi 0,10 maka sistem akan melakukan Auto Consistency sebelum menghitung bobot Fuzzy AHP.
    """
    )
    
    criteria = [
                "Biaya",
                "Performa",
                "Skalabilitas",
                "Keamanan",
                "Reliability"
            ]
    
    matrix_user = np.array([
        [1,      b_p,      b_s,      b_k,      b_r],
        [1/b_p,  1,        p_s,      p_k,      p_r],
        [1/b_s,  1/p_s,    1,        s_k,      s_r],
        [1/b_k,  1/p_k,    1/s_k,    1,        k_r],
        [1/b_r,  1/p_r,    1/s_r,    1/k_r,    1]
    ])

    return matrix_user, criteria