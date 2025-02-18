import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=5b6afc844f5a794b71751b52888997bb&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

similarity=pickle.load(open('similarity.pkl','rb'))
movies=pickle.load(open('movies.pkl','rb'))

st.title("Movie Recommendation System")

option = st.selectbox(
    "Put the movie name",
    movies['title'].values
)

if st.button("Recommended"):
    recommended_movie_names, recommended_movie_posters = recommend(option)
    col = st.columns(5)
    for i in range(5):
        with col[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])


