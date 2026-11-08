import numpy as np 
import pandas as pd 
import requests

movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb5000_credits.csv')



movies = movies.merge(credits,on='title')



# --- main dataframe ----
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
movies.dropna(inplace=True)

import ast
def convert(obj):
    L =[]
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

movies['genres'] = movies['genres'].apply(convert)


movies['keywords'] = movies['keywords'].apply(convert)



def convert3(obj):
    L =[]
    counter = 0
    for i in ast.literal_eval(obj):
        if(counter != 3):
            L.append(i['name'])
            counter +=1
        else:
            break
    return L

movies['cast'] = movies['cast'].apply(convert3)


movies['overview'] = movies['overview'].apply(lambda x:x.split())


movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])


movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']


new_df = movies[['movie_id','title','tags']]


new_df['tags'] = new_df['tags'].apply(lambda x:" ".join(x))
new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())


import nltk
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))

    return " ".join(y)

new_df['tags'] = new_df['tags'].apply(stem)

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words = 'english')

vector = cv.fit_transform(new_df['tags']).toarray()


from sklearn.metrics.pairwise import cosine_similarity


similarity = cosine_similarity(vector)

def fetch_poster(i):
  response =  requests.get(f'https://api.themoviedb.org/3/movie/{i}?api_key={}&language=en-US')

  data = response.json()
  return ("https://image.tmdb.org/t/p/w500/" + data['poster_path'])

def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse = True , key = lambda x:x[1])[0:10]
    result = []
    movie_names = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # result.append(i[0])
        result.append(fetch_poster(movie_id))
        movie_names.append(new_df.iloc[i[0]].title)
  
    
    return result,movie_names






moviess = new_df['title'].tolist()


