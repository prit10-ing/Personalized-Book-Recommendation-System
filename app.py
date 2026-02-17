import os
import pickle
import numpy as np
from flask import Flask, render_template, request, session

from books_recommender.config.configuration import AppConfiguration
from books_recommender.pipeline.training_pipeline import TrainingPipeline


# =====================================================
# APP INIT
# =====================================================
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")


# =====================================================
# RECOMMENDATION ENGINE
# =====================================================
class Recommendation:
    def __init__(self, app_config=AppConfiguration()):
        self.config = app_config.get_recommendation_config()

        self.book_pivot = None
        self.final_rating = None

        self._load_base_objects()

    def _load_base_objects(self):
        """Load heavy pickle files once."""
        try:
            self.book_pivot = pickle.load(
                open(self.config.book_pivot_serialized_objects, "rb")
            )
            self.final_rating = pickle.load(
                open(self.config.final_rating_serialized_objects, "rb")
            )
            print("✅ Base recommendation objects loaded")
        except Exception as e:
            print("❌ Failed loading base objects:", e)

    def fetch_poster(self, suggestion):
        posters = []
        names = [self.book_pivot.index[i] for i in suggestion[0]]

        for name in names:
            try:
                idx = np.where(self.final_rating["title"] == name)[0][0]
                posters.append(self.final_rating.iloc[idx]["image_url"])
            except Exception:
                posters.append(
                    "https://via.placeholder.com/150x220.png?text=No+Image"
                )

        return posters

    def recommend(self, book_name):
        model_path = self.config.trained_model_path

        if not os.path.exists(model_path):
            return None, None

        try:
            model = pickle.load(open(model_path, "rb"))
            book_id = np.where(self.book_pivot.index == book_name)[0][0]
        except Exception:
            return None, None

        _, suggestion = model.kneighbors(
            self.book_pivot.iloc[book_id, :].values.reshape(1, -1),
            n_neighbors=6,
        )

        books = self.book_pivot.index[suggestion[0]].tolist()
        posters = self.fetch_poster(suggestion)

        return books, posters


# Create engine ONCE
rec_engine = Recommendation()


# =====================================================
# ROUTES
# =====================================================
@app.route("/", methods=["GET", "POST"])
def home():
    if "favorites" not in session:
        session["favorites"] = []

    # Load book names
    try:
        book_names = pickle.load(open("templates/book_names.pkl", "rb"))
    except Exception:
        book_names = []

    recommended = None
    posters = None
    message = None

    if request.method == "POST":
        action = request.form.get("action")

        # ---------------- TRAIN ----------------
        if action == "train":
            try:
                pipe = TrainingPipeline()
                pipe.start_training_pipeline()
                message = "Training completed successfully!"
            except Exception:
                message = "Training failed. Check logs."

        # ---------------- RECOMMEND ----------------
        elif action == "recommend":
            selected = request.form.get("book")
            recommended, posters = rec_engine.recommend(selected)

            if recommended is None:
                message = "Model not available. Train first."

        # ---------------- FAVORITE ----------------
        elif action == "favorite":
            book = request.form.get("book")
            favs = session["favorites"]

            if book and book not in favs:
                favs.append(book)
                session["favorites"] = favs
                message = "Added to favorites ❤️"

    return render_template(
        "index.html",
        book_names=book_names,
        recommended=recommended,
        posters=posters,
        favorites=session["favorites"],
        message=message,
    )


# =====================================================
# HEALTH CHECK (Render loves this)
# =====================================================
@app.route("/health")
def health():
    return {"status": "ok"}


# =====================================================
# LOCAL RUN
# =====================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    print("\n" + "=" * 60)
    print(f"🚀 BOOK RECOMMENDER RUNNING ON PORT {port}")
    print("=" * 60 + "\n")

    app.run(host="0.0.0.0", port=port, debug=True,use_reloader=False)
