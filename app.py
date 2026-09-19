import streamlit as st
import pandas as pd
import requests
import html

from src.recommender import recommend_movies, movies


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="CineMatch AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# OMDb API
# =========================================================

OMDB_API_KEY = "28ca0725"


# =========================================================
# POSTER FUNCTION
# =========================================================

@st.cache_data(show_spinner=False)
def get_poster(movie_title):

    clean_title = movie_title.split("(")[0].strip()

    try:

        response = requests.get(
            "https://www.omdbapi.com/",
            params={
                "apikey": OMDB_API_KEY,
                "t": clean_title,
                "type": "movie"
            },
            timeout=10
        )

        if response.status_code != 200:
            return None

        data = response.json()

        if data.get("Response") != "True":
            return None

        poster = data.get("Poster")

        if poster and poster != "N/A":
            return poster

    except Exception:
        return None

    return None


# =========================================================
# LOAD RATINGS
# =========================================================

ratings = pd.read_csv("data/ratings.csv")

avg_ratings = (
    ratings
    .groupby("movieId")["rating"]
    .mean()
    .reset_index()
)

avg_ratings.columns = [
    "movieId",
    "avg_rating"
]


# Add ratings only once
if "avg_rating" not in movies.columns:

    movies = movies.merge(
        avg_ratings,
        on="movieId",
        how="left"
    )


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def get_year(title):

    if "(" in title and ")" in title:

        return (
            title
            .split("(")[-1]
            .replace(")", "")
        )

    return "N/A"


def get_rating(title):

    row = movies[
        movies["title"] == title
    ]

    if row.empty:
        return "N/A"

    rating = row.iloc[0]["avg_rating"]

    if pd.isna(rating):
        return "N/A"

    return round(float(rating), 2)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>

/* =========================================================
   GLOBAL
   ========================================================= */

.stApp {
    background: #050914;
    color: #F4F4F6;
}

.main {
    background: #050914;
}

.block-container {
    max-width: 1500px;

    padding-top: 1.3rem;
    padding-bottom: 2rem;

    padding-left: 2.2rem;
    padding-right: 2.2rem;
}

header {
    background: transparent !important;
}

#MainMenu {
    visibility: hidden;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {

    background: #080E1B;

    border-right: 1px solid #1D2739;

    min-width: 310px;
    max-width: 310px;
}

section[data-testid="stSidebar"] > div {

    padding: 1.3rem 1.1rem;
}


/* =========================================================
   SIDEBAR BRAND
   ========================================================= */

.brand-wrapper {

    display: flex;

    align-items: center;

    gap: 11px;

    margin-bottom: 22px;
}

.brand-icon {

    width: 42px;
    height: 42px;

    display: flex;

    align-items: center;
    justify-content: center;

    background: rgba(193, 18, 47, 0.14);

    border: 1px solid
        rgba(193, 18, 47, 0.30);

    border-radius: 11px;

    font-size: 22px;
}

.brand-name {

    color: #F5F5F7;

    font-size: 19px;

    font-weight: 800;

    line-height: 1.1;
}

.brand-sub {

    color: #858B99;

    font-size: 12px;

    margin-top: 4px;
}


/* =========================================================
   SIDEBAR NAV
   ========================================================= */

section[data-testid="stSidebar"]
div[role="radiogroup"] {

    gap: 3px;
}

section[data-testid="stSidebar"]
div[role="radiogroup"] label {

    border-radius: 9px;

    padding: 7px 9px;

    border: 1px solid transparent;
}

section[data-testid="stSidebar"]
div[role="radiogroup"] label:hover {

    background: #121827;
}

section[data-testid="stSidebar"]
div[role="radiogroup"] label p {

    color: #C7CAD2 !important;

    font-size: 14px;
}


/* =========================================================
   SIDEBAR CARDS
   ========================================================= */

.side-card {

    background: #0C1321;

    border: 1px solid #1E293D;

    border-radius: 13px;

    padding: 15px;

    margin-top: 13px;
}

.side-title {

    color: #F3F4F6;

    font-size: 14px;

    font-weight: 700;

    margin-bottom: 7px;
}

.side-text {

    color: #969BA8;

    font-size: 12px;

    line-height: 1.55;
}


/* =========================================================
   HERO
   ========================================================= */

.hero-title {

    font-size: 31px;

    font-weight: 800;

    letter-spacing: -0.8px;

    color: #F5F5F7;

    margin-top: 0px;

    margin-bottom: 1px;

    line-height: 1.15;
}

.hero-accent {

    color: #C1122F;
}

.hero-subtitle {

    color: #9298A7;

    font-size: 14px;

    margin-top: 2px;

    margin-bottom: 12px;

    line-height: 1.3;
}


/* =========================================================
   SELECTOR
   ========================================================= */

.selector-card {

    background: #0B1220;

    border: 1px solid #1E2A40;

    border-radius: 14px;

    padding: 14px 24px;

    margin-top: 0px;

    margin-bottom: -5px;
}

.selector-heading {

    color: #F3F4F6;

    font-size: 16px;

    font-weight: 700;
}

.selector-description {

    color: #8F94A2;

    font-size: 12px;

    margin-top: 3px;
}


/* =========================================================
   SELECT BOX
   ========================================================= */

div[data-baseweb="select"] > div {

    background: #080E19 !important;

    border: 1px solid #263249 !important;

    border-radius: 9px !important;

    min-height: 47px;
}

div[data-baseweb="select"] > div:hover {

    border-color: #C1122F !important;
}

div[data-baseweb="select"] span {

    color: #ECEEF2 !important;
}

div[data-baseweb="select"] input {

    color: white !important;
}

div[role="listbox"] {

    background: #0B1220 !important;

    border: 1px solid #263249 !important;
}

div[role="option"] {

    color: #D7D9E0 !important;
}

div[role="option"]:hover {

    background: #17121A !important;
}


/* =========================================================
   BUTTON
   ========================================================= */

div.stButton > button {

    width: 100%;

    min-height: 47px;

    background:
        linear-gradient(
            90deg,
            #8F1024,
            #C1122F
        );

    color: #FFFFFF !important;

    border: 1px solid #D21F3C;

    border-radius: 9px;

    font-size: 14px;

    font-weight: 750;

    box-shadow:
        0 5px 18px
        rgba(193,18,47,0.18);

    transition: 0.2s ease;
}

div.stButton > button:hover {

    background:
        linear-gradient(
            90deg,
            #A30F27,
            #E01B3D
        );

    border-color: #F02A4A;

    transform: translateY(-1px);

    box-shadow:
        0 8px 24px
        rgba(193,18,47,0.32);
}


/* =========================================================
   SELECTED MOVIE HEADER
   ========================================================= */

.selected-card {

    background:
        linear-gradient(
            100deg,
            #0D1728,
            #110D1C
        );

    border: 1px solid #202C43;

    border-radius: 13px;

    padding: 12px 19px;

    height: 76px;

    display: flex;

    flex-direction: column;

    justify-content: center;
}

.selected-small {

    color: #A1A4B0;

    font-size: 12px;
}

.selected-title {

    color: #D21F3C;

    font-size: 19px;

    font-weight: 800;

    margin-top: 2px;
}


/* =========================================================
   ALGORITHM
   ========================================================= */

.algorithm {

    background: #17111F;

    border: 1px solid #30223D;

    border-radius: 10px;

    padding: 10px 14px;

    height: 76px;

    display: flex;

    flex-direction: column;

    justify-content: center;
}

.algorithm-label {

    color: #9497A3;

    font-size: 10px;
}

.algorithm-value {

    color: #D21F3C;

    font-size: 13px;

    font-weight: 700;

    margin-top: 3px;
}


/* =========================================================
   MOVIE CARD
   ========================================================= */

.movie-card {

    position: relative;

    background: #0A111E;

    border: 1px solid #1E2A3D;

    border-radius: 12px;

    overflow: hidden;

    transition: 0.2s ease;
}

.movie-card:hover {

    transform: translateY(-4px);

    border-color:
        rgba(193,18,47,0.55);

    box-shadow:
        0 15px 35px
        rgba(0,0,0,0.35);
}


/* =========================================================
   RANK
   ========================================================= */

.rank {

    position: absolute;

    z-index: 10;

    top: 9px;

    left: 9px;

    width: 34px;

    height: 34px;

    display: flex;

    align-items: center;

    justify-content: center;

    background:
        linear-gradient(
            135deg,
            #D21F3C,
            #8B1022
        );

    color: white;

    border-radius: 9px;

    font-size: 13px;

    font-weight: 800;
}


/* =========================================================
   POSTER
   ========================================================= */

.poster {

    width: 100%;

    height: 285px;

    object-fit: cover;

    display: block;

    background: #101725;
}

.no-poster {

    width: 100%;

    height: 285px;

    display: flex;

    align-items: center;

    justify-content: center;

    background: #101725;

    color: #777D8B;

    font-size: 13px;

    text-align: center;
}


/* =========================================================
   MOVIE INFO
   ========================================================= */

.movie-info {

    padding: 12px;
}

.movie-name {

    color: #F2F3F5;

    font-size: 14px;

    font-weight: 700;

    white-space: nowrap;

    overflow: hidden;

    text-overflow: ellipsis;
}

.movie-year {

    color: #858A99;

    font-size: 12px;

    margin-top: 3px;

    margin-bottom: 10px;
}


/* =========================================================
   RATING
   ========================================================= */

.rating-box {

    display: flex;

    justify-content: space-between;

    align-items: center;

    background: #15111C;

    border: 1px solid #292034;

    border-radius: 8px;

    padding: 8px 9px;
}

.rating-label {

    color: #9699A6;

    font-size: 10px;
}

.rating-value {

    color: #D21F3C;

    font-size: 13px;

    font-weight: 800;
}


/* =========================================================
   AI BAR
   ========================================================= */

.ai-bar {

    display: flex;

    justify-content: space-between;

    align-items: center;

    background:
        linear-gradient(
            100deg,
            #0C1422,
            #100D18
        );

    border: 1px solid #202B40;

    border-radius: 13px;

    padding: 14px 18px;

    margin-top: 16px;
}

.ai-left {

    display: flex;

    align-items: center;

    gap: 12px;
}

.ai-icon {

    width: 42px;

    height: 42px;

    display: flex;

    align-items: center;

    justify-content: center;

    background:
        rgba(193,18,47,0.14);

    border: 1px solid
        rgba(193,18,47,0.28);

    border-radius: 50%;

    font-size: 20px;
}

.ai-message {

    color: #B2B4BF;

    font-size: 12px;
}

.feedback {

    color: #A5A8B3;

    font-size: 12px;

    text-align: right;

    border-left: 1px solid #273043;

    padding-left: 25px;
}

.feedback-accent {

    color: #D21F3C;
}


/* =========================================================
   FOOTER
   ========================================================= */

.custom-footer {

    text-align: center;

    color: #666B78;

    font-size: 11px;

    padding: 22px 0 5px;
}


/* =========================================================
   SLIDER
   ========================================================= */

div[data-testid="stSlider"] div[role="slider"] {

    background: #C1122F !important;
}


/* =========================================================
   DIVIDER
   ========================================================= */

hr {

    border-color: #1B2639 !important;
}


/* =========================================================
   HIDE DEFAULT LABELS
   ========================================================= */

div[data-testid="stSelectbox"] > label {

    display: none;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 900px) {

    .block-container {

        padding-left: 1rem;

        padding-right: 1rem;
    }

}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.html(
        """
        <div class="brand-wrapper">

            <div class="brand-icon">
                🎬
            </div>

            <div>

                <div class="brand-name">
                    CineMatch AI
                </div>

                <div class="brand-sub">
                    Recommendation System
                </div>

            </div>

        </div>
        """
    )


    page = st.radio(
        "Navigation",
        [
            "🏠  Home",
            "☆  Recommendations",
            "🏆  Top Rated Movies",
            "▣  Explore Movies",
            "ⓘ  About Project"
        ],
        label_visibility="collapsed"
    )


    st.divider()


    st.html(
        """
        <div class="side-card">

            <div class="side-title">
                Number of Recommendations
            </div>

            <div class="side-text">
                Choose how many similar movies
                you want to see.
            </div>

        </div>
        """
    )


    number_of_recommendations = st.slider(
        "Number of Recommendations",
        min_value=1,
        max_value=10,
        value=5,
        label_visibility="collapsed"
    )


    st.html(
        """
        <div class="side-card">

            <div class="side-title">
                How It Works
            </div>

            <div class="side-text">

                🖱️ &nbsp;
                <b>1. You select a movie</b>

                <br><br>

                🧠 &nbsp;
                <b>2. Our AI analyzes movie patterns</b>

                <br><br>

                💡 &nbsp;
                <b>3. Get top-rated recommendations</b>

            </div>

        </div>
        """
    )


# =========================================================
# HOME PAGE
# =========================================================

if "Home" in page:

    # =====================================================
    # HERO
    # =====================================================

    st.html(
        """
        <div class="hero-title">

            🎬
            <span class="hero-accent">
                CineMatch AI
            </span>

        </div>

        <div class="hero-subtitle">

            A Movie Recommendation System

        </div>
        """
    )


    # =====================================================
    # SELECTOR HEADER
    # =====================================================

    st.html(
        """
        <div class="selector-card">

            <div class="selector-heading">
                Select a Movie
            </div>

            <div class="selector-description">
                Choose a movie you like
            </div>

        </div>
        """
    )


    # =====================================================
    # MOVIE SELECT + BUTTON
    # =====================================================

    select_col, button_col = st.columns(
        [5, 1],
        gap="medium"
    )


    with select_col:

        selected_movie = st.selectbox(
            "Movie",
            movies["title"].values,
            label_visibility="collapsed"
        )


    with button_col:

        recommend_clicked = st.button(
            "✨ Recommend",
            use_container_width=True
        )


    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    if recommend_clicked:

        with st.spinner(
            "Finding recommendations..."
        ):

            recommendations = recommend_movies(
                selected_movie
            )


        recommendations = list(
            recommendations
        )


        # Remove selected movie
        recommendations = [
            movie
            for movie in recommendations
            if movie != selected_movie
        ]


        recommendations = recommendations[
            :number_of_recommendations
        ]


        # =================================================
        # SELECTED MOVIE HEADER
        # =================================================

        left, right = st.columns(
            [4, 1],
            gap="medium"
        )


        with left:

            st.html(
                f"""
                <div class="selected-card">

                    <div class="selected-small">

                        🍿
                        Top {len(recommendations)}
                        Recommendations for

                    </div>

                    <div class="selected-title">

                        {html.escape(
                            str(selected_movie)
                        )}

                    </div>

                </div>
                """
            )


        with right:

            st.html(
                """
                <div class="algorithm">

                    <div class="algorithm-label">
                        Algorithm Used
                    </div>

                    <div class="algorithm-value">
                        Rating-Based Filtering
                    </div>

                </div>
                """
            )


        st.write("")


        # =================================================
        # MOVIE CARDS
        # =================================================

        if recommendations:

            cols = st.columns(
                len(recommendations),
                gap="small"
            )


            for i, movie in enumerate(
                recommendations
            ):

                movie = str(movie)

                poster = get_poster(
                    movie
                )

                year = get_year(
                    movie
                )

                rating = get_rating(
                    movie
                )


                movie_safe = html.escape(
                    movie
                )


                # -----------------------------------------
                # POSTER
                # -----------------------------------------

                if poster:

                    poster_safe = html.escape(
                        poster,
                        quote=True
                    )

                    poster_html = f"""
                    <img
                        src="{poster_safe}"
                        class="poster"
                    >
                    """

                else:

                    poster_html = """
                    <div class="no-poster">
                        🎬<br>
                        Poster unavailable
                    </div>
                    """


                # -----------------------------------------
                # CARD
                # -----------------------------------------

                with cols[i]:

                    st.html(
                        f"""
                        <div class="movie-card">

                            <div class="rank">
                                {i + 1}
                            </div>

                            {poster_html}

                            <div class="movie-info">

                                <div class="movie-name">
                                    {movie_safe}
                                </div>

                                <div class="movie-year">
                                    {year}
                                </div>

                                <div class="rating-box">

                                    <span class="rating-label">
                                        Average Rating
                                    </span>

                                    <span class="rating-value">
                                        ⭐ {rating}/5
                                    </span>

                                </div>

                            </div>

                        </div>
                        """
                    )


        else:

            st.info(
                "No recommendations found."
            )


        # =================================================
        # AI MESSAGE
        # =================================================

        st.html(
            """
            <div class="ai-bar">

                <div class="ai-left">

                    <div class="ai-icon">
                        🤖
                    </div>

                    <div class="ai-message">

                        Our AI analyzes movie patterns
                        and user ratings to recommend
                        movies you'll love!

                    </div>

                </div>

                <div class="feedback">

                    👍 &nbsp;
                    Like this recommendation?

                    <br>

                    <span class="feedback-accent">
                        Give it a feedback!
                    </span>

                </div>

            </div>
            """
        )


# =========================================================
# RECOMMENDATIONS PAGE
# =========================================================

elif "Recommendations" in page:

    st.html(
        """
        <div class="hero-title">

            🎬
            <span class="hero-accent">
                Recommendations
            </span>

        </div>

        <div class="hero-subtitle">

            Discover movies based on your selection.

        </div>
        """
    )


    selected_movie = st.selectbox(
        "Select a movie",
        movies["title"].values
    )


    if st.button(
        "✨ Recommend"
    ):

        recommendations = list(
            recommend_movies(
                selected_movie
            )
        )


        recommendations = [
            movie
            for movie in recommendations
            if movie != selected_movie
        ]


        recommendations = recommendations[
            :number_of_recommendations
        ]


        if recommendations:

            cols = st.columns(
                len(recommendations),
                gap="small"
            )


            for i, movie in enumerate(
                recommendations
            ):

                movie = str(movie)

                poster = get_poster(
                    movie
                )

                year = get_year(
                    movie
                )

                rating = get_rating(
                    movie
                )


                movie_safe = html.escape(
                    movie
                )


                if poster:

                    poster_safe = html.escape(
                        poster,
                        quote=True
                    )

                    poster_html = f"""
                    <img
                        src="{poster_safe}"
                        class="poster"
                    >
                    """

                else:

                    poster_html = """
                    <div class="no-poster">
                        🎬<br>
                        Poster unavailable
                    </div>
                    """


                with cols[i]:

                    st.html(
                        f"""
                        <div class="movie-card">

                            <div class="rank">
                                {i + 1}
                            </div>

                            {poster_html}

                            <div class="movie-info">

                                <div class="movie-name">
                                    {movie_safe}
                                </div>

                                <div class="movie-year">
                                    {year}
                                </div>

                                <div class="rating-box">

                                    <span class="rating-label">
                                        Average Rating
                                    </span>

                                    <span class="rating-value">
                                        ⭐ {rating}/5
                                    </span>

                                </div>

                            </div>

                        </div>
                        """
                    )


# =========================================================
# TOP RATED MOVIES
# =========================================================

elif "Top Rated" in page:

    st.html(
        """
        <div class="hero-title">

            ⭐
            <span class="hero-accent">
                Top Rated Movies
            </span>

        </div>

        <div class="hero-subtitle">

            Explore the highest-rated movies
            in the dataset.

        </div>
        """
    )


    top_movies = (
        movies
        .dropna(
            subset=["avg_rating"]
        )
        .sort_values(
            "avg_rating",
            ascending=False
        )
        .head(10)
    )


    cols = st.columns(
        5,
        gap="small"
    )


    for i, (_, movie_data) in enumerate(
        top_movies.iterrows()
    ):

        movie = str(
            movie_data["title"]
        )

        poster = get_poster(
            movie
        )

        rating = round(
            float(
                movie_data["avg_rating"]
            ),
            2
        )

        year = get_year(
            movie
        )


        movie_safe = html.escape(
            movie
        )


        if poster:

            poster_safe = html.escape(
                poster,
                quote=True
            )

            poster_html = f"""
            <img
                src="{poster_safe}"
                class="poster"
            >
            """

        else:

            poster_html = """
            <div class="no-poster">
                🎬<br>
                Poster unavailable
            </div>
            """


        with cols[i % 5]:

            st.html(
                f"""
                <div class="movie-card">

                    <div class="rank">
                        {i + 1}
                    </div>

                    {poster_html}

                    <div class="movie-info">

                        <div class="movie-name">
                            {movie_safe}
                        </div>

                        <div class="movie-year">
                            {year}
                        </div>

                        <div class="rating-box">

                            <span class="rating-label">
                                Average Rating
                            </span>

                            <span class="rating-value">
                                ⭐ {rating}/5
                            </span>

                        </div>

                    </div>

                </div>
                """
            )


# =========================================================
# EXPLORE MOVIES
# =========================================================

elif "Explore" in page:

    st.html(
        """
        <div class="hero-title">

            🔎
            <span class="hero-accent">
                Explore Movies
            </span>

        </div>

        <div class="hero-subtitle">

            Search movies from the dataset.

        </div>
        """
    )


    search = st.text_input(
        "Search movies",
        placeholder="Search for a movie..."
    )


    if search:

        results = movies[
            movies["title"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ].head(20)


        for _, row in results.iterrows():

            movie = str(
                row["title"]
            )

            rating = get_rating(
                movie
            )

            genres = row["genres"]


            st.markdown(
                f"""
                **{movie}**

                ⭐ {rating}/5

                {genres}
                """
            )

            st.divider()


# =========================================================
# ABOUT PROJECT
# =========================================================

elif "About" in page:

    st.html(
        """
        <div class="hero-title">

            ℹ️
            <span class="hero-accent">
                About CineMatch AI
            </span>

        </div>

        <div class="hero-subtitle">

            A Movie Recommendation System

        </div>
        """
    )


    st.markdown(
        """
        ### 🎬 CineMatch AI

        CineMatch AI is a machine-learning based
        movie recommendation system built using
        Python, Pandas, Scikit-learn and Streamlit.

        The system analyzes movie data and ratings
        to generate personalized movie recommendations.
        """
    )


# =========================================================
# FOOTER
# =========================================================

st.html(
    """
    <div class="custom-footer">

        © 2026 AI Movie Recommendation System
        &nbsp; | &nbsp;
        Built with ❤️ using Streamlit

    </div>
    """
)