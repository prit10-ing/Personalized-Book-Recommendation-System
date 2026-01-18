import os
import sys
import pickle
import streamlit as st
import numpy as np
from books_recommender.logger.log import logging
from books_recommender.config.configuration import AppConfiguration
from books_recommender.pipeline.training_pipeline import TrainingPipeline
from books_recommender.exception.exception_handler import AppException

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="📚 Book Recommender System",
    page_icon="📖",
    layout="wide"
)

# ================= SESSION STATE =================
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# ================= CUSTOM CSS =================
st.markdown("""
<style>
body {
    background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364);
    background-size: 400% 400%;
    animation: gradientBG 12s ease infinite;
}

@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

.fade-in {
    animation: fadeIn 1.4s ease-in;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(15px);}
    to {opacity: 1; transform: translateY(0);}
}

.card {
    background: #1c1f26;
    border-radius: 16px;
    padding: 15px;
    text-align: center;
    transition: all 0.3s ease;
}

.card:hover {
    transform: scale(1.05);
    box-shadow: 0 12px 30px rgba(255, 140, 0, 0.45);
}

.book-title {
    font-weight: 600;
    color: white;
    margin-bottom: 6px;
}

.rating {
    color: gold;
    font-size: 15px;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("<h1 style='text-align:center;'>📚 Personalized Book Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Collaborative Filtering • Machine Learning • Streamlit</p>", unsafe_allow_html=True)
st.markdown("---")


# ================= MAIN CLASS =================
class Recommendation:
    def __init__(self, app_config=AppConfiguration()):
        try:
            self.recommendation_config = app_config.get_recommendation_config()
        except Exception as e:
            raise AppException(e, sys)

    def fetch_poster(self, suggestion):
        try:
            poster_url = []
            book_pivot = pickle.load(open(self.recommendation_config.book_pivot_serialized_objects, 'rb'))
            final_rating = pickle.load(open(self.recommendation_config.final_rating_serialized_objects, 'rb'))

            book_names = [book_pivot.index[i] for i in suggestion[0]]

            for name in book_names:
                idx = np.where(final_rating['title'] == name)[0][0]
                poster_url.append(final_rating.iloc[idx]['image_url'])

            return poster_url
        except Exception as e:
            raise AppException(e, sys)

    def recommend_book(self, book_name):
        try:
            model_path = self.recommendation_config.trained_model_path

            if not os.path.exists(model_path):
                st.warning("⚠️ Model not found. Please train the recommender system first.")
                return None, None

            model = pickle.load(open(model_path, 'rb'))
            book_pivot = pickle.load(open(self.recommendation_config.book_pivot_serialized_objects, 'rb'))

            book_id = np.where(book_pivot.index == book_name)[0][0]
            _, suggestion = model.kneighbors(
                book_pivot.iloc[book_id, :].values.reshape(1, -1),
                n_neighbors=6
            )

            poster_url = self.fetch_poster(suggestion)
            books_list = book_pivot.index[suggestion[0]].tolist()

            return books_list, poster_url
        except Exception as e:
            raise AppException(e, sys)

    def train_engine(self):
        try:
            with st.spinner("🔄 Training model... please wait"):
                obj = TrainingPipeline()
                obj.start_training_pipeline()
            st.success("✅ Training completed successfully!")
            logging.info("Training completed")
        except Exception as e:
            raise AppException(e, sys)

    def recommendations_engine(self, selected_books):
        books, posters = self.recommend_book(selected_books)

        if books is None:
            return

        st.markdown("## ✨ Recommended Books")
        cols = st.columns(5)

        for i in range(1, 6):
            with cols[i - 1]:
                rating = round(np.random.uniform(3.6, 5.0), 1)
                stars = "⭐" * int(rating)

                st.markdown(f"""
                <div class="card fade-in">
                    <div class="book-title">{books[i]}</div>
                    <div class="rating">{stars} ({rating})</div>
                </div>
                """, unsafe_allow_html=True)

                st.image(posters[i], use_column_width=True)

                if st.button("❤️ Save to Favorites", key=f"fav_{i}"):
                    if books[i] not in st.session_state.favorites:
                        st.session_state.favorites.append(books[i])


# ================= APP FLOW =================
obj = Recommendation()

st.markdown("### 🧠 Step 1: Train the Model")
st.info("If this is your first time, click **Train Recommender System**.")

if st.button("🚀 Train Recommender System"):
    obj.train_engine()

st.markdown("---")

st.markdown("### 🔍 Step 2: Search Book (Autocomplete Enabled)")
book_names = pickle.load(open(os.path.join('templates', 'book_names.pkl'), 'rb'))

selected_books = st.selectbox(
    "Type book name",
    book_names
)

st.markdown("### 🎯 Step 3: Get Recommendations")
if st.button("✨ Show Recommendations"):
    obj.recommendations_engine(selected_books)

# ================= FAVORITES =================
st.markdown("---")
st.markdown("## ❤️ Your Favorite Books")

if st.session_state.favorites:
    for book in st.session_state.favorites:
        st.success(book)
else:
    st.info("No favorites yet. Start exploring 📚")
