import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY")

def get_poster(movie_name):
    url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={movie_name}"
    
    response = requests.get(url)
    data = response.json()
    
    if data.get("Response") == "True" and data.get("Poster") != "N/A":
        return data.get("Poster")
            
    return None