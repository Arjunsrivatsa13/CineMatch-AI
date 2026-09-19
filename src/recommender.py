import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv("data/movies.csv")

movies["genres"] = movies["genres"].fillna("")

tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(movies["genres"])

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)


def recommend_movies(movie_title, num_recommendations=5):
    matches = movies[
        movies["title"].str.contains(
            movie_title,
            case=False,
            na=False,
            regex=False
        )
    ]

    if matches.empty:
        return []

    movie_index = matches.index[0]

    similarity_scores = list(enumerate(cosine_sim[movie_index]))

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    movie_indices = [
        i[0] for i in similarity_scores[1:num_recommendations + 1]
    ]

    return movies.iloc[movie_indices]["title"].tolist()