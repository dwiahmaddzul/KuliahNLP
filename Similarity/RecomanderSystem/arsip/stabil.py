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
    recommendations = data.iloc[similarity_scores.argsort()[::-1]]
    recommendations = recommendations[~recommendations['title'].isin(read_articles)]
    return recommendations.head(top_n)

# Rekomendasi berdasarkan daftar bacaan
def recommend_multiple(read_texts, vectorizer, vectors, data, read_articles, top_n=5):
    user_vectors = vectorizer.transform(read_texts)
    avg_vector = user_vectors.mean(axis=0)
    avg_vector = np.asarray(avg_vector)  # Konversi ke numpy array
    similarity_scores = cosine_similarity(avg_vector, vectors).flatten()
    recommendations = data.iloc[similarity_scores.argsort()[::-1]]
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

    # Pilih artikel
    st.sidebar.header("Pilih Artikel")
    article_title = st.sidebar.selectbox("Artikel yang ingin dibaca:", data['title'])
    article = data[data['title'] == article_title].iloc[0]

    # Tampilkan artikel
    st.subheader(article['title'])
    paragraphs = split_paragraphs(article['content'])
    for paragraph in paragraphs:
        st.write(paragraph.strip())
        st.write("")  # Tambahkan jarak antar paragraf

    # Session State untuk daftar bacaan
    if 'read_articles' not in st.session_state:
        st.session_state['read_articles'] = []

    # Tambahkan artikel ke daftar bacaan
    if article_title not in st.session_state['read_articles']:
        st.session_state['read_articles'].append(article_title)

    # Tampilkan daftar bacaan
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
            st.write(f"### {row['title']}")
            st.write(row['content'][:100] + "...")
    else:
        st.write("Belum ada rekomendasi saat ini.")

if __name__ == "__main__":
    main()