import streamlit as st

def home_page():
    st.title("Selamat Datang di Aplikasi Rekomendasi Berita 📚")
    st.write(
        """
        **Aplikasi Berita dengan Rekomendasi** ini dirancang untuk memberikan pengalaman membaca yang lebih personal dan efisien. 
        Dengan menggunakan teknologi *Machine Learning* berbasis **TF-IDF** dan **cosine similarity**, aplikasi ini memberikan rekomendasi artikel yang sesuai dengan minat kamu.
        """
    )

    st.subheader("🔍 Fitur Utama")
    st.write(
        """
        - **Baca Artikel Terbaru**: Jelajahi artikel dari berbagai topik menarik.
        - **Rekomendasi Personal**: Dapatkan rekomendasi artikel berdasarkan bacaan kamu.
        - **Daftar Bacaan**: Lacak artikel yang sudah kamu baca.
        - **Reset Bacaan**: Mulai dari awal kapan saja dengan menghapus daftar bacaan.
        """
    )

    st.subheader("🛠️ Cara Menggunakan")
    st.write(
        """
        1. **Pilih Artikel** dari sidebar untuk mulai membaca.
        2. Artikel yang kamu baca akan otomatis masuk ke daftar bacaan.
        3. Lihat rekomendasi artikel yang relevan di bagian bawah.
        4. Gunakan tombol reset di sidebar untuk menghapus daftar bacaan.
        """
    )

    st.subheader("📖 Tentang Aplikasi")
    st.write(
        """
        Aplikasi ini dibuat untuk membantu kamu menemukan artikel yang relevan dan meningkatkan pengalaman membaca berita. 
        Teknologi yang digunakan meliputi:
        - **TF-IDF**: Untuk memahami isi artikel.
        - **Cosine Similarity**: Untuk menghitung kemiripan antar artikel.
        """
    )

    st.write("✨ **Selamat Membaca!** ✨")
