# AI Movie Recommendation System

A content-based movie recommendation platform built with Python, FastAPI, and Scikit-Learn. This application recommends movies similar to your selection and dynamically fetches movie posters from the TMDB API.

## 🧠 The Machine Learning Pipeline (Model Building Process)

The core of this platform is a **Content-Based Filtering** recommendation engine. It suggests movies similar to a user's choice by analyzing metadata rather than relying on historical user interaction data.

### 1. Data Collection & Preprocessing
The model is trained using the **TMDB 5000 Movies & Credits dataset**. The training process begins by merging the movies and credits datasets based on the movie title. We filter down the features to keep only the most impactful textual columns: `movie_id`, `title`, `overview`, `genres`, `keywords`, `cast`, and `crew`.

### 2. Feature Engineering
Raw JSON-like string data is parsed and transformed to extract relevant tags:
- **Genres & Keywords**: Extracted directly as lists of descriptive words.
- **Cast**: Limited to the top 3 actors to prioritize main cast members.
- **Crew**: Filtered specifically to extract the **Director**.

We apply a `collapse` function to remove spaces between multi-word names (e.g., "Science Fiction" becomes "ScienceFiction", "Johnny Depp" becomes "JohnnyDepp"). This ensures our model treats a full name or specific phrase as a single unique entity, avoiding overlap between "Johnny Depp" and "Johnny Galecki".

### 3. Text Vectorization & Stemming
All engineered features are combined with the movie `overview` to create a massive `tags` column representing the entire identity of the movie. 
- **Stemming (NLTK)**: We use the `PorterStemmer` to reduce words to their root forms (e.g., "loving", "loved", "lover" become "love"). This reduces the dimensionality of our data and groups semantically similar words.
- **CountVectorizer (Scikit-Learn)**: We convert the text data into numerical vectors. We limit the vocabulary to the top 5,000 most frequent words and remove standard English stop words.

### 4. Similarity Calculation
With all movies mapped as points in a 5000-dimensional vector space, we calculate the **Cosine Similarity** between every movie. The closer the cosine angle is to 1, the more similar the movies are. The resulting distance matrix is serialized using `pickle` into `similarity.pkl` for rapid, real-time inference in production.

---

## 💻 The Web Application (Development & Architecture)

To serve the machine learning model to users, we built a monolithic, server-side rendered web application. 

### Backend (FastAPI & Python)
- **Framework**: Powered by **FastAPI** (`app.py`), chosen for its high performance and ease of use in serving Python-based APIs.
- **Model Inference**: The backend utilizes `recommendation.py` to load the serialized `movies.pkl` metadata and the `similarity.pkl` matrix via Python's built-in `pickle` module. When a user requests a recommendation, it queries the similarity matrix to instantly find the top 5 closest matches.
- **External API Integration**: For a richer user experience, the system makes live HTTP requests (via the `requests` library) to the **TMDB (The Movie Database) API** to fetch high-resolution movie posters dynamically based on the recommended movie IDs. Environment variables are managed securely using `python-dotenv`.

### Frontend (Jinja2 & HTML/CSS)
- **Server-Side Rendering**: The UI is built using standard HTML/CSS and is rendered on the server side using the **Jinja2** templating engine. 
- **User Flow**: When you navigate to the home page (`/`), FastAPI injects the full list of available movies into the `index.html` dropdown menu.
- **Interaction**: Selecting a movie and hitting "Recommend" triggers a standard HTML form submission (a `POST` request to the `/recommend` route). The backend calculates the recommendations, fetches the posters, and re-renders the HTML page with the new customized movie cards injected directly into the template.

---

## 🚀 Installation & Setup

1. Clone the repository and navigate to the project directory.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your environment variables:
   Create a `.env` file in the root directory and add your TMDB API key:
   ```env
   TMDB_API_KEY=your_api_key_here
   ```
5. Run the FastAPI server:
   ```bash
   uvicorn app:app --reload
   ```
6. Open your browser and navigate to `http://127.0.0.1:8000`.
