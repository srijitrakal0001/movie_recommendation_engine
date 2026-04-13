import pickle
import streamlit as st
import requests
import pandas as pd  # Ensure pandas is imported

# Load the movie data and similarity matrix
movies_dict = pickle.load(open(r'E:\Movie_Recommendation_System\ML_Model\movies_dict.pkl' , 'rb'))
movies = pd.DataFrame(movies_dict)  # Convert dictionary to DataFrame

similarity = pickle.load(open(r'E:\Movie_Recommendation_System\ML_Model\similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return None  # Return None if no poster is found

def recommend(movie):
    if movie not in movies['title'].values:
        return [], []  # Return empty lists if the movie is not found

    index = movies[movies['title'] == movie].index[0]
    distances = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:11]:  # Skip the first element as it's the selected movie itself
        movie_id = movies.iloc[i[0]].movie_id
        poster_url = fetch_poster(movie_id)
        if poster_url:  # Only add if a valid poster is found
            recommended_movie_posters.append(poster_url)
            recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Streamlit UI
st.header('Movie Recommender System')

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    if not recommended_movie_names:  # If no movies are returned
        st.error("Movie not found in the database. Please select a valid movie.")
    else:
        cols = st.columns(5)
        for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
            with col:
                st.text(name)
                st.image(poster)