import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


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

    st.subheader("Keterbatasan")
    st.write(
        """
        Saat ini aplikasi tidak lagi didukung st.experimental_rerun sehingga "Baca Selengkapnya" dan beberapa tombol harus diklik dua kali.
        Code by : Dwi Ahmad Dzulhijjah
        """
    )

    st.write("✨ **Selamat Membaca!** ✨")

@st.cache_data
def load_data():
    return pd.read_json('berita.json')

@st.cache_data
def compute_tfidf(data):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(data['content'])
    return vectorizer, vectors

def recommend_single(article_text, vectorizer, vectors, data, read_articles, top_n=5):
    user_vector = vectorizer.transform([article_text])
    similarity_scores = cosine_similarity(user_vector, vectors).flatten()
    recommendations = data.iloc[similarity_scores.argsort()[::-1]].copy()
    recommendations['similarity'] = similarity_scores[recommendations.index]
    recommendations = recommendations[~recommendations['title'].isin(read_articles)]
    return recommendations.head(top_n)

def recommend_multiple(read_texts, vectorizer, vectors, data, read_articles, top_n=5):
    user_vectors = vectorizer.transform(read_texts)
    avg_vector = user_vectors.mean(axis=0)
    avg_vector = np.asarray(avg_vector)
    similarity_scores = cosine_similarity(avg_vector, vectors).flatten()
    recommendations = data.iloc[similarity_scores.argsort()[::-1]].copy()
    recommendations['similarity'] = similarity_scores[recommendations.index]
    recommendations = recommendations[~recommendations['title'].isin(read_articles)]
    return recommendations.head(top_n)

def split_paragraphs(content):
    return content.split('. ')

def read_news_page(pilihan):
    data = load_data()
    vectorizer, vectors = compute_tfidf(data)

    if 'read_articles' not in st.session_state:
        st.session_state['read_articles'] = []
    if 'selected_article' not in st.session_state:
        st.session_state['selected_article'] = data['title'].iloc[0]

    st.sidebar.header("Pilih Artikel")
    article_title = st.sidebar.selectbox(
        "Artikel yang ingin dibaca:",
        data['title'],
        index=int(data[data['title'] == st.session_state['selected_article']].index[0])
    )
    st.session_state['selected_article'] = article_title

    article = data[data['title'] == st.session_state['selected_article']].iloc[0]

    st.subheader(article['title'])
    for paragraph in split_paragraphs(article['content']):
        st.write(paragraph.strip())
        st.write("")

    if article_title not in st.session_state['read_articles']:
        st.session_state['read_articles'].append(article_title)

    st.sidebar.subheader("Daftar Bacaan Kamu")
    for read_title in st.session_state['read_articles']:
        st.sidebar.write("- " + read_title)

    if st.sidebar.button("Reset Bacaan"):
        st.session_state['read_articles'] = []

    st.subheader("Mungkin Kamu Suka")
    read_articles = st.session_state['read_articles']

    if len(read_articles) == 1:
        recommendations = recommend_single(article['content'], vectorizer, vectors, data, read_articles)
    elif len(read_articles) > 1:
        read_texts = data[data['title'].isin(read_articles)]['content'].tolist()
        recommendations = recommend_multiple(read_texts, vectorizer, vectors, data, read_articles)
    else:
        recommendations = pd.DataFrame()

    if not recommendations.empty:
        for _, row in recommendations.iterrows():
            col1, col2 = st.columns([4, 1])
            with col1:
                if pilihan =="Tampilkan" :
                    st.write(f"### {row['title']} (Skor: {row['similarity']:.2f})")
                else :
                    st.write(f"### {row['title']}")
                st.write(row['content'][:100] + "...")
            with col2:
                if st.button(f"Baca Selengkapnya", key=row['title']):
                    st.session_state['selected_article'] = row['title']
    else:
        st.write("Belum ada rekomendasi saat ini.")

def main():
    st.sidebar.title("Navigasi")
    page = st.sidebar.radio("Pilih Halaman", ["Beranda", "Baca Berita", "Tampilkan Similarity"])

    if page == "Beranda":
        home_page()
    elif page == "Baca Berita":
        read_news_page(pilihan=None)
    elif page == "Tampilkan Similarity":
        read_news_page(pilihan="Tampilkan")

if __name__ == "__main__":
    main()