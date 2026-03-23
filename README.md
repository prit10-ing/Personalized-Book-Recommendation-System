# 📚 Personalized Book Recommendation System

A **Collaborative Filtering–based Book Recommendation System** built using **Machine Learning**.
This project recommends books to users based on similarity between user preferences using the **K-Nearest Neighbors (KNN) algorithm**.

The system analyzes historical user-book interactions and identifies similar books using collaborative filtering techniques.


---

# 🚀 Features

* 📖 Personalized book recommendations
* 🤖 Machine Learning–based recommendation system
* 🔎 Uses **K-Nearest Neighbors (KNN)** similarity algorithm
* ❤️ Favorite books saving system
* 🌐 Interactive web interface using **Flask**
* ⚡ Fast recommendations using pre-trained model

---

# 🧠 Machine Learning Approach

This project uses **Collaborative Filtering**, which recommends books based on user interaction patterns.

### Steps used in the model

1. Collect user-book rating dataset
2. Clean and preprocess the data
3. Create a **User–Book Pivot Table**
4. Convert pivot table to sparse matrix
5. Train **K-Nearest Neighbors model**
6. Serialize trained model using **Pickle**
7. Use the model to recommend similar books

### Algorithm Used

**K-Nearest Neighbors (KNN)**

The model finds the most similar books by measuring distance between book vectors in the pivot table.

Similarity is calculated using:

* **/ Euclidean Distance**

The system returns the **top 5 most similar books** to the selected book.

---

# 🛠 Tech Stack

* Python
* Flask
* Scikit-learn
* Pandas
* NumPy
* HTML / CSS
* Pickle
* Docker (optional for deployment)

---


---

# ⚙️ Installation

### 1️⃣ Clone the repository

```
git clone https://github.com/your-username/book-recommendation-system.git
```

```
cd book-recommendation-system
```

---

### 2️⃣ Create virtual environment

```
python -m venv venv
```

Activate environment

**Windows**

```
venv\Scripts\activate
```

**Mac/Linux**

```
source venv/bin/activate
```

---

### 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

---
RUN main.py file 


# ▶️ Run the Application

Run the Flask application:

```
python app.py
```

The application will start on:

```
http://localhost:5000
```

Open the URL in your browser and start getting book recommendations.

---

# 🌐 Deployment


For deployment, the trained model files (`.pkl`) are stored inside the **artifacts folder**, so the system loads the model directly without retraining.

---

# 📸 Demo

Users can:

1. Select a book
2. Click **Recommend**
3. Get top recommended books
4. Save favorite books

---

# 📌 Future Improvements

* Add user login system
* Improve recommendation accuracy
* Add hybrid recommendation system
* Use deep learning recommendation models

---

# 👨‍💻 Author

**Pritesh**

Data Science Enthusiast | Machine Learning Developer
