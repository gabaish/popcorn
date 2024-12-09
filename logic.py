#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix



# In[2]:


movies = pd.read_csv('data/movies.csv')
ratings = pd.read_csv('data/ratings.csv')


# In[3]:


merged_data = pd.merge(ratings, movies, on='movieId') #merging the data of ratings and movies


# In[4]:


# # remove users with less than 50 reviews
user_review_counts = merged_data['userId'].value_counts()
filtered_users = user_review_counts[user_review_counts > 50].index
filtered_data = merged_data[merged_data['userId'].isin(filtered_users)]

# # remove movies with less than 100 reviews
movie_review_counts = filtered_data['title'].value_counts()
filtered_movies = movie_review_counts[movie_review_counts > 100].index
filtered_data = filtered_data[filtered_data['title'].isin(filtered_movies)]

# sparse user-movie matrix
row = filtered_data['userId'].astype('category').cat.codes #users
col = filtered_data['title'].astype('category').cat.codes #movies
data = filtered_data['rating'].values #ratings
user_movie_sparse = csr_matrix((data, (row, col)))


# In[5]:


# mapping movie titles to their corresponding colums in the sparse matrix 
title_to_index = dict(enumerate(filtered_data['title'].astype('category').cat.categories))
index_to_title = {v: k for k, v in title_to_index.items()}


# In[6]:


# computing movie similarity based on user ratings
model = NearestNeighbors(metric='cosine', algorithm='brute')
model.fit(user_movie_sparse.T) # rows represent movies, columns represent users


# In[7]:


def recommend_movies_by_title_nn(movie_title, model, user_movie_sparse, top_n=5):
    # check if the movie exists in the mapping
    if movie_title not in index_to_title:
        return f"Movie '{movie_title}' not found."

    # get the index of the movie in the sparse matrix
    movie_idx = index_to_title[movie_title]

    # find the nearest neighbors (most similar movies)
    distances, indices = model.kneighbors(user_movie_sparse.T[movie_idx], n_neighbors=top_n + 1)

    # returning the top N similar movies
    similar_movies = [(title_to_index[i], distances[0][j]) for j, i in enumerate(indices[0]) if i != movie_idx]

    return similar_movies[:top_n]


# In[8]:


def recommend_for_two_users_with_five_results(user1_movie, user2_movie):
    top_n = 5 # num of recommendations
    # recommendations for User 1
    user1_recommendations = recommend_movies_by_title_nn(user1_movie, model, user_movie_sparse, top_n * 2)

    # recommendations for User 2
    user2_recommendations = recommend_movies_by_title_nn(user2_movie, model, user_movie_sparse, top_n * 2)

    user1_recommendations_set = set([rec[0] for rec in user1_recommendations])
    user2_recommendations_set = set([rec[0] for rec in user2_recommendations])

    # checking for common recommendations between the two users
    common_recommendations = user1_recommendations_set.intersection(user2_recommendations_set)

    # if there are >= 5 recommendations
    if len(common_recommendations) >= top_n:
        return list(common_recommendations)[:top_n]

    # if there are less than 5 recommendations, we will rank all their recommended movies based on their combined similarity score
    combined_scores = {}
    # iterating on user 1 recommended movies, and for each, coverting the cosine distance (dist) into similarity using 1 - dist
    for movie, dist in user1_recommendations:
        combined_scores[movie] = 1 - dist  
    
    # iterating on user 1 recommended movies, and for each, adding its similarity (1 - dist) 
    for movie, dist in user2_recommendations:
        combined_scores[movie] = combined_scores.get(movie, 0) + (1 - dist)

    # storing the combined movies recommendations in a descending order of te similarity scores, and returning the top 5 movies
    ranked_recommendations = sorted(combined_scores, key=combined_scores.get, reverse=True)
    return ranked_recommendations[:top_n]


# In[11]:


# Input movies from two users
#user1_movie = "Toy Story (1995)"
#user2_movie = "Forrest Gump (1994)"

# Get guaranteed top 5 recommendations for both users
#recommendations = recommend_for_two_users_with_five_results(user1_movie, user2_movie)
#print("Top 5 Recommendations for Both Users:")
#print(recommendations)


# In[ ]:




