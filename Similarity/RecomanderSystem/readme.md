# 📚 Aplikasi Rekomendasi Berita Berbasis Machine Learning

Aplikasi ini adalah sistem rekomendasi berita berbasis **Machine Learning** yang dirancang untuk memberikan pengalaman membaca yang personal dan relevan. Menggunakan **TF-IDF** dan **cosine similarity**, aplikasi ini menganalisis konten artikel untuk memberikan rekomendasi yang sesuai dengan preferensi pengguna.

---

## 🎯 Fitur Utama
- **Baca Artikel Terbaru**: Jelajahi artikel dari berbagai kategori.
- **Rekomendasi Artikel**: Dapatkan rekomendasi artikel berdasarkan artikel yang sudah dibaca.
- **Daftar Bacaan**: Lacak artikel yang sudah Anda baca.
- **Reset Bacaan**: Mulai dari awal kapan saja dengan fitur reset.

---

## 🛠️ Teknologi yang Digunakan
- **[Streamlit](https://streamlit.io/)**: Framework Python untuk membangun aplikasi web interaktif.
- **Pandas**: Untuk manipulasi dan pengolahan data.
- **Scikit-learn**: Untuk implementasi TF-IDF dan cosine similarity.
- **NumPy**: Untuk perhitungan vektor dan manipulasi matriks.

---

## 🚀 Cara Menggunakan
1. **Clone Repository**
   ```bash
   git clone `github.com/dwiahmaddzul/KuliahNLP/edit/main/Similarity/RecomanderSystem.git`
   cd RecomanderSystem
   ```

2. **Install Dependencies**
   Pastikan Python 3.7+ sudah terinstal di perangkat Anda. Lalu, jalankan:
   ```bash
   pip install -r requirements.txt
   ```

3. **Siapkan Dataset**
   Tambahkan file `berita.json` ke root directory. File ini harus berisi data dalam format berikut:
   ```json
   [
       {
           "title": "Judul Artikel 1",
           "content": "Isi artikel 1."
       },
       {
           "title": "Judul Artikel 2",
           "content": "Isi artikel 2."
       }
   ]
   ```

4. **Jalankan Aplikasi**
   ```bash
   streamlit run app.py
   ```

5. **Navigasi di Aplikasi**
   - **Beranda**: Lihat informasi tentang aplikasi.
   - **Baca Berita**: Pilih dan baca artikel, dapatkan rekomendasi personal.
   - **Tampilkan Similarity**: Tampilkan skor kemiripan artikel berdasarkan konten.

---

## 🎨 Struktur Folder
```plaintext
.
├── app.py                # Script utama aplikasi Streamlit
├── berita.json           # Dataset artikel dalam format JSON
├── requirements.txt      # Daftar dependensi
└── README.md             # Dokumentasi proyek
```

---

## 🔍 Catatan Penting
- Aplikasi menggunakan caching dengan `@st.cache_data` untuk meningkatkan performa.
- Fitur **reset** memungkinkan pengguna untuk menghapus daftar bacaan dan memulai ulang kapan saja.
- Pastikan dataset memiliki konten artikel yang cukup untuk mendapatkan rekomendasi yang optimal.

---

## ✨ Kontributor
Dibuat oleh **Dwi Ahmad Dzulhijjah**.  
Jika ada masukan atau pertanyaan, jangan ragu untuk membuat *issue* atau menghubungi saya melalui email.

---

## 📜 Lisensi
Aplikasi ini dirilis di bawah lisensi [MIT License](LICENSE). Anda bebas untuk menggunakan, memodifikasi, dan mendistribusikan proyek ini selama mengikuti ketentuan lisensi.
