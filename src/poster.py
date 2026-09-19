import requests

API_KEY = "YOUR_TMDB_API_KEY"

def get_poster(movie_name):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"

    response = requests.get(url)
    data = response.json()

    if data.get("results"):
        poster_path = data["results"][0].get("poster_path")

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"

    return None