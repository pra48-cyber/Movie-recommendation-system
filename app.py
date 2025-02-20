import streamlit as st
import pickle
import requests

# TMDB API Key
API_KEY = "5b6afc844f5a794b71751b52888997bb"
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return "https://via.placeholder.com/150"  # Placeholder image if no poster found

# Function to fetch movie trailer
def fetch_trailer(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}"
    data = requests.get(url).json()

    trailers = [video for video in data.get("results", []) if video["type"] == "Trailer" and video["site"] == "YouTube"]

    if trailers:
        return f"https://www.youtube.com/watch?v={trailers[0]['key']}"
    return None  # No trailer found

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_trailers = []

    for i in distances[1:6]:  # Get top 5 recommendations
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_trailers.append(fetch_trailer(movie_id))

    return recommended_movie_names, recommended_movie_posters, recommended_movie_trailers

# Load similarity matrix and movies dataframe
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pickle.load(open('movies.pkl', 'rb'))

# Streamlit UI
st.title("🎬 Movie Recommendation System")

# Movie selection dropdown
option = st.selectbox("Enter a movie name:", movies['title'].values)

# Initialize variables before using them
recommended_movie_names = []
recommended_movie_posters = []
recommended_movie_trailers = []

if st.button("Recommend"):
    recommended_movie_names, recommended_movie_posters, recommended_movie_trailers = recommend(option)

    # Display recommendations in columns
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(recommended_movie_names[i])  # Bold Movie Name
            st.image(recommended_movie_posters[i], use_container_width=True)  # Movie Poster

# **Add a Trailer Section Header**
st.markdown("### 🎥 Trailers of Recommended Movies")

# Ensure we only display trailers if they exist
if recommended_movie_trailers:
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            if recommended_movie_trailers[i]:
                st.video(recommended_movie_trailers[i])
            else:
                st.write("No trailer available")
