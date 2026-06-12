from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from recommendation import recommend
import pickle

# Initialize FastAPI
app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates folder
templates = Jinja2Templates(directory="templates")

# Load movies data
movies = pickle.load(open('movies.pkl', 'rb'))


# Home Page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    movie_list = movies['title'].values.tolist()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "movies": movie_list
        }
    )


# Recommendation Route
@app.post("/recommend", response_class=HTMLResponse)
async def get_recommendation(
    request: Request,
    movie: str = Form(...)
):

    # Get recommendations and posters
    recommended_movies, recommended_posters = recommend(movie)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "movies": movies['title'].values.tolist(),
            "recommendations": recommended_movies,
            "posters": recommended_posters,
            "selected_movie": movie
        }
    )