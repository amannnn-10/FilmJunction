import streamlit as st
import pickle
import pandas as pd
import requests
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

# Set up session state
class SessionState:
    def __init__(self):
        self.username = None

session_state = SessionState()

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=388e934d9b3d581e339633ceab2d83bb&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movie_list:
        movie_id =  movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # Fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

movies_list = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
movies_list = movies['title'].values

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Movie Recommender System")

if st.button('Sign in with Google'):
    # Get user token
    token = st.text_input('Enter your Google Sign-In token:')
    if token:
        try:
            id_info = id_token.verify_oauth2_token(token, google_requests.Request(), '839753753062-5i6iaceiphg5jd92f6bk9fhmmip3a43g.apps.googleusercontent.com')
            session_state.username = id_info['email']
            st.success(f'Successfully signed in as {session_state.username}')
        except Exception as e:
            st.error('Authentication failed. Please try again.')

selected_movie_name = st.selectbox('Select a movie:', movies_list)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])