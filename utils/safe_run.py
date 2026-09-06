# utils/safe_run.py
"""
Helper agar setiap halaman/tahap tidak perlu menulis blok
try/except sendiri-sendiri.

Dengan safe_run(), perlindungan dipakai di
halaman mana pun (fuzzy_ahp_page, topsis_page, dst) cukup
dengan membungkus pemanggilan fungsinya, tanpa menulis ulang
try/except di setiap file.

Contoh pemakaian, di app.py atau app_user.py:

    from utils.safe_run import safe_run

    active_matrix, consistency_result = safe_run(
        show_consistency,
        matrix_user,
        criteria,
        _fallback_pesan="Gagal menguji konsistensi matriks.",
    )

Jika show_consistency() melempar exception, safe_run akan
menampilkan st.error(...) dengan pesan yang jelas, lalu
menghentikan eksekusi halaman saat ini (st.stop()) sehingga
tahap-tahap berikutnya tidak dijalankan dengan data yang
tidak lengkap/rusak.
"""

import streamlit as st


def safe_run(func, *args, _fallback_pesan=None, **kwargs):
    """
    Menjalankan `func(*args, **kwargs)` dengan perlindungan
    try/except. Jika terjadi error, tampilkan pesan ramah lalu
    hentikan eksekusi halaman (st.stop()).

    Args:
        func            : fungsi yang akan dijalankan.
        *args, **kwargs : argumen untuk `func`.
        _fallback_pesan : pesan singkat yang ditampilkan ke
                          pengguna sebelum detail teknis error.
                          Jika None, dipakai pesan generik.

    Returns:
        Hasil dari func(*args, **kwargs), apa pun bentuknya
        (tuple, dict, dll) — sama seperti memanggil func
        secara langsung, tapi lebih aman.

    Catatan: fungsi ini memanggil st.stop() jika terjadi
    error, sehingga baris kode SETELAH pemanggilan safe_run()
    yang gagal tidak akan pernah dieksekusi pada run tersebut.
    """

    pesan = _fallback_pesan or (
        "Terjadi kendala saat memproses tahap ini."
    )

    try:
        return func(*args, **kwargs)

    except Exception as e:
        st.error(
            f"{pesan}\n\n"
            f"Detail teknis: {e}"
        )
        st.stop()