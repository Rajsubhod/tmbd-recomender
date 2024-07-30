import streamlit as st
import joblib
import pandas as pd
import requests

# Load the model
try:
    movies_list = joblib.load('./notebook/movies_dict.pkl')
    movies_list = pd.DataFrame(movies_list)

    sim = joblib.load('./notebook/similarity.pkl')

except Exception as e:
    st.error(e)

def recomend(movie):
  movie_index=movies_list[movies_list['title']==movie].index[0]
  similarity = sim[movie_index]
  mol=sorted(list(enumerate(similarity)),reverse=True,key=lambda x:x[1])[1:6]
  
  title = []
  for i in mol:
    t=[]
    t.append(movies_list.iloc[i[0]].movie_id)
    t.append(movies_list.iloc[i[0]].title)
    title.append(t)
  return title

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id, '8265bd1679663a7ea12ac168da84d2e8'))

    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

if __name__ == '__main__':
    # Title
    st.title('Movie Recommendation System')

    mv = movies_list['title']
    # st.write(mv)

    # Select box
    selected_movie = st.selectbox('Select a movie:', mv)

    if st.button('Recommend'):
        cols = st.columns(5)
        for _,i in enumerate(recomend(selected_movie)):
            with cols[_]:
                st.image(fetch_poster(i[0]))
                st.write(str(i[1]))
