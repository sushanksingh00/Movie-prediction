from fastapi import FastAPI
import pickle
import requests
import urllib.parse


similarity_mat = pickle.load(open("similarity.pkl", "rb"))
df = pickle.load(open("movies.pkl", "rb"))

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_route():
    return {"Hello": "root"}


def recommend(movie):
    movie_index = df[df["title"] == movie].index[0]
    movie_list_title = []
    distances = similarity_mat[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key = lambda x : x[1])[1:101] #excluding the first(itself)
    count = 0
    for i in movie_list:
        # dictt = {}
        # dictt["title"] = df.iloc[i[0]].title
        # dictt["details"] = get_details(df.iloc[i[0]].title)
        details = get_details(df.iloc[i[0]].title)
        if not details == None:
            movie_list_title.append(details)
            count += 1
        if count == 5:
            break
    return movie_list_title

@app.get("/recommend")
def recommend_api(movie: str):
    return recommend(movie)
     

API_KEY = "47ccc6b6fe76986e304586db8b35fe02"


def get_details(title):

    title = urllib.parse.quote(title)
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}"
    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=5
        )
        data = response.json()
        if "results" not in data or len(data["results"]) == 0:
            return None

        movie = data["results"][0]
        poster = None
        if movie["poster_path"]:
            poster = "https://image.tmdb.org/t/p/w500" + movie["poster_path"]

        return {
            "title": movie.get("title"),
            "overview": movie.get("overview"),
            "rating": movie.get("vote_average"),
            "poster": poster
        }
    except Exception as e:
        print("TMDb API error:", e)
        return None