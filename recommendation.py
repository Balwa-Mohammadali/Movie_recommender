import pickle
import pandas as pd
import requests

# Load saved files
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))



from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")


# Fetch poster from TMDB
def fetch_poster(movie_id):

    try:

        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

        response = requests.get(url, timeout=10)

        data = response.json()

        # Check if poster exists
        if data.get('poster_path'):

            poster_path = data['poster_path']

            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path

            return full_path

        else:

            return "https://via.placeholder.com/500x750?text=No+Poster"

    except requests.exceptions.RequestException as e:

        print("TMDB Error:", e)

        return "https://via.placeholder.com/500x750?text=Connection+Error"


# Recommendation function
def recommend(movie):

    # Find selected movie index
    movie_index = movies[movies['title'] == movie].index[0]

    # Get similarity scores
    distances = similarity[movie_index]

    # Sort movies
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    # Fetch recommended movies
    for i in movies_list:

        index = i[0]

        # Movie title
        title = movies.iloc[index].title

        # Movie ID
        movie_id = movies.iloc[index].movie_id

        # Append movie title
        recommended_movies.append(title)

        # Append poster
        recommended_posters.append(
            fetch_poster(movie_id)
        )

    return recommended_movies, recommended_posters