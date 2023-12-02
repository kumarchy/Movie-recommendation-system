import pickle
import streamlit as st
import pandas as pd
import requests

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500"+data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance=similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])

    recommended_movies=[]
    recommended_movies_poster=[]
    for i in movies_list[1:7]:
        movie_id=movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from api
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster

st.header('Movie Recommender System')
movies_dict=pickle.load(open('movie_list.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl','rb'))

selected_movie_name = st.selectbox(
    "Type or select a movie from the dropdown",
    (movies['title'].values)
)
if st.button('Recommend'):
    
    ##---This is for recommending the movie in single row and multiple columns----
    
    # names,posters=recommend(selected_movie_name)
    # col1, col2, col3, col4, col5,col6,col7 = st.columns(7)
    # with col1:
    #     st.text(names[0])
    #     st.image(posters[0])
    # with col2:
    #     st.text(names[1])
    #     st.image(posters[1])
    #
    # with col3:
    #     st.text(names[2])
    #     st.image(posters[2])
    # with col4:
    #     st.text(names[3])
    #     st.image(posters[3])
    # with col5:
    #     st.text(names[4])
    #     st.image(posters[4])
    # with col6:
    #     st.text(names[1,5])
    #     st.image(posters[1,5])
    # with col7:
    #     st.text(names[1,6])
    #     st.image(posters[1,6])

    
    ##---This is for recommending the movie in multiple row and multiple columns----
    names, posters = recommend(selected_movie_name)

    # Assuming each row has 3 items (adjust accordingly based on your layout)
    items_per_row = 3

    # Calculate the number of rows needed
    num_rows = (len(names) - 1) // items_per_row + 1

    # Loop through each row
    for row in range(num_rows):
        # Create columns for each item in the row
        columns = st.columns(items_per_row)

        # Loop through each column in the row
        for col_index in range(items_per_row):
            # Calculate the index of the item in the original list
            item_index = row * items_per_row + col_index

            # Check if the index is within the range of the list
            if item_index < len(names):
                with columns[col_index]:
                    st.text(names[item_index])
                    st.image(posters[item_index])



