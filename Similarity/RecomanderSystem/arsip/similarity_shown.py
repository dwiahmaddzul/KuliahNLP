import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load data dari file JSON
@st.cache_data
def load_data():
    return pd.read_json('berita.json')

# Hitung vektor TF-IDF sekali untuk efisiensi
@st.cache_data
def compute_tfidf(data):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(data['content'])
    return vectorizer, vectors

# Rekomendasi berdasarkan satu artikel
def recommend_single(article_text, vectorizer, vectors, data, read_articles, top_n=5):
    user_vector = vectorizer.transform([article_text])
    similarity_scores = cosine_similarity(user_vector, vectors).flatten()
    recommendations = data.iloc[similarity_scores.argsort()[::-1]].copy()
    recommendations['similarity'] = similarity_scores[recommendations.index]
    recommendations = recommendations[~recommendations['title'].isin(read_articles)]
    return recommendations.head(top_n)

# Rekomendasi berdasarkan daftar bacaan
def recommend_multiple(read_texts, vectorizer, vectors, data, read_articles, top_n=5):
    user_vectors = vectorizer.transform(read_texts)
    avg_vector = user_vectors.mean(axis=0)  # Ini menghasilkan objek np.matrix
    avg_vector = np.asarray(avg_vector)  # Ubah ke numpy array
    similarity_scores = cosine_similarity(avg_vector, vectors).flatten()
    recommendations = data.iloc[similarity_scores.argsort()[::-1]].copy()
    recommendations['similarity'] = similarity_scores[recommendations.index]
    recommendations = recommendations[~recommendations['title'].isin(read_articles)]
    return recommendations.head(top_n)

# Fungsi untuk memecah paragraf berdasarkan titik
def split_paragraphs(content):
    paragraphs = content.split('. ')
    return paragraphs

# Streamlit App
def main():
    st.title("Aplikasi Berita dengan Rekomendasi")

    # Load data
    data = load_data()
    vectorizer, vectors = compute_tfidf(data)

    # Session State untuk daftar bacaan dan artikel yang dipilih
    if 'read_articles' not in st.session_state:
        st.session_state['read_articles'] = []
    if 'selected_article' not in st.session_state:
        st.session_state['selected_article'] = data['title'].iloc[0]  # Artikel default

    # Sidebar: Pilih artikel
    st.sidebar.header("Pilih Artikel")
    article_title = st.sidebar.selectbox(
        "Artikel yang ingin dibaca:",
        data['title'],
        index=int(data[data['title'] == st.session_state['selected_article']].index[0])  # Pastikan tipe int
    )
    st.session_state['selected_article'] = article_title

    # Artikel yang dipilih
    article = data[data['title'] == st.session_state['selected_article']].iloc[0]

    # Tampilkan artikel utama
    st.subheader(article['title'])
    paragraphs = split_paragraphs(article['content'])
    for paragraph in paragraphs:
        st.write(paragraph.strip())
        st.write("")  # Tambahkan jarak antar paragraf

    # Tambahkan artikel ke daftar bacaan
    if article_title not in st.session_state['read_articles']:
        st.session_state['read_articles'].append(article_title)

    # Sidebar: Daftar bacaan
    st.sidebar.subheader("Daftar Bacaan Kamu")
    for read_title in st.session_state['read_articles']:
        st.sidebar.write("- " + read_title)

    # Tombol reset daftar bacaan
    if st.sidebar.button("Reset Bacaan"):
        st.session_state['read_articles'] = []

    # Rekomendasi
    st.subheader("Mungkin Kamu Suka")
    read_articles = st.session_state['read_articles']

    if len(read_articles) == 1:
        current_article_text = article['content']
        recommendations = recommend_single(current_article_text, vectorizer, vectors, data, read_articles)
    elif len(read_articles) > 1:
        read_texts = data[data['title'].isin(read_articles)]['content'].tolist()
        if read_texts:
            recommendations = recommend_multiple(read_texts, vectorizer, vectors, data, read_articles)
        else:
            recommendations = pd.DataFrame()
    else:
        recommendations = pd.DataFrame()

    # Tampilkan rekomendasi
    if not recommendations.empty:
        for _, row in recommendations.iterrows():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"### {row['title']} (Skor: {row['similarity']:.2f})")
                st.write(row['content'][:100] + "...")
            with col2:
                if st.button(f"Baca Selengkapnya", key=row['title']):
                    st.session_state['selected_article'] = row['title']

    else:
        st.write("Belum ada rekomendasi saat ini.")

if __name__ == "__main__":
    main()