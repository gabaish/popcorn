import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds
from scipy.sparse import csr_matrix
import requests
import re

# Load data at module level
movies2 = pd.read_csv('data/movies3.csv')
ratings = pd.read_csv('data/ratings.csv')

# Merge ratings with movies to ensure we only use movies that exist in both datasets
merged_df = pd.merge(ratings, movies2, on='movieId', how='inner')

# Create sparse matrix using csr_matrix
def create_matrix(df):
    N = len(df['userId'].unique())
    M = len(df['movieId'].unique())
    
    # Map Ids to array indices
    user_mapper = dict(zip(np.unique(df["userId"]), list(range(N))))
    movie_mapper = dict(zip(np.unique(df["movieId"]), list(range(M))))
    
    # Map indices to IDs
    user_inv_mapper = dict(zip(list(range(N)), np.unique(df["userId"])))
    movie_inv_mapper = dict(zip(list(range(M)), np.unique(df["movieId"])))
    
    user_index = [user_mapper[i] for i in df['userId']]
    movie_index = [movie_mapper[i] for i in df['movieId']]
    
    X = csr_matrix((df["rating"], (user_index, movie_index)), shape=(N, M))
    
    return X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper

# Create the sparse matrix and get the mappers
X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper = create_matrix(merged_df)

# Perform SVD
U, sigma, Vt = svds(X, k=50)
sigma = np.diag(sigma)

# Create title to index mapping
title_to_movieId = dict(zip(movies2['title'], movies2['movieId']))
movieId_to_title = dict(zip(movies2['movieId'], movies2['title']))

# Get the index of a movie in the SVD matrix
def get_movie_index(movie_title):
    if movie_title not in title_to_movieId:
        return None
    movie_id = title_to_movieId[movie_title]
    if movie_id not in movie_mapper:
        return None
    return movie_mapper[movie_id]

# Find similar movies using SVD latent features
def find_similar_movies_svd(movie_title, n_recommendations=5):
    movie_idx = get_movie_index(movie_title)
    if movie_idx is None:
        return []
    
    # Get the latent features for the movie
    movie_features = Vt[:, movie_idx]
    
    # Calculate similarity with all other movies
    similarities = np.dot(Vt.T, movie_features)
    
    # Get indices of top similar movies
    similar_indices = np.argsort(similarities)[::-1][1:n_recommendations + 1]
    
    # Convert indices back to movie titles
    similar_movies = []
    for idx in similar_indices:
        movie_id = movie_inv_mapper[idx]
        if movie_id in movieId_to_title:
            # movie_title = movieId_to_title[movie_id]
            # similarity_score = similarities[idx]
            # similar_movies.append((movie_title, similarity_score))
            similar_movies.append(movieId_to_title[movie_id])
    
    return similar_movies

# Generate recommendations based on two input movies using SVD
def recommend_for_two_users_with_five_results_svd(movie1, movie2):
    # Get recommendations for both movies
    recommendations1 = find_similar_movies_svd(movie1, n_recommendations=10)
    recommendations2 = find_similar_movies_svd(movie2, n_recommendations=10)
    
    # Convert to sets for easier manipulation
    rec_set1 = set(recommendations1)
    rec_set2 = set(recommendations2)
    
    # Find common recommendations
    common_recommendations = rec_set1.intersection(rec_set2)
    
    # If we have enough common recommendations, use them
    if len(common_recommendations) >= 5:
        return list(common_recommendations)[:5]
    
    # Otherwise, combine unique recommendations and sort by similarity
    all_recommendations = list(rec_set1.union(rec_set2))
    
    # Calculate combined similarity scores
    combined_scores = {}
    for movie in all_recommendations:
        score1 = recommendations1.index(movie) if movie in recommendations1 else len(recommendations1)
        score2 = recommendations2.index(movie) if movie in recommendations2 else len(recommendations2)
        combined_scores[movie] = -(score1 + score2)  # Negative because lower indices are better
    
    # Sort by combined score
    sorted_recommendations = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
    recommendations = [movie for movie, _ in sorted_recommendations[:5]]
    
    print("Top 5 SVD recommendations:", recommendations)
    # Return top 5 recommendations
    return recommendations

# TMDB API 
TMDB_API_KEY = "f9c68fee291e011281ee8722f40fbc18"
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

# Normalize movie titles by removing articles and year
def normalize_title(title):
    clean_title = re.sub(r"\s\(\d{4}\)$", "", title)
    clean_title = re.sub(r"^(The|A|An)\s", "", clean_title, flags=re.IGNORECASE)
    return clean_title.strip()

# Fetches the poster URL and summary for a given movie title using TMDb API
def get_movie_poster_tmdb(title):
    match = re.search(r"\((\d{4})\)$", title)
    year = match.group(1) if match else None
    clean_title = normalize_title(title)

    queries = [
        {"query": title, "year": year},
        {"query": clean_title, "year": year},
        {"query": title},
        {"query": clean_title}
    ]
    
    for params in queries:
        params['api_key'] = TMDB_API_KEY
        search_url = f"{TMDB_BASE_URL}/search/movie"
        response = requests.get(search_url, params=params)
        data = response.json()
        
        if response.status_code == 200 and data['results']:
            result = data['results'][0]
            poster_path = result.get('poster_path')
            summary = result.get('overview', 'No summary available.')
            poster_url = (
                f"https://image.tmdb.org/t/p/w500{poster_path}" 
                if poster_path 
                else None
            )
            return poster_url, summary
    
    return None, 'No summary available'

# Generate recommendations based on multiple input movies using SVD.
def recommend_for_multiple_movies(movie_list, n_recommendations=5):
    if not movie_list:
        return []
    
    if len(movie_list) == 1:
        return find_similar_movies_svd(movie_list[0], n_recommendations=n_recommendations)
    
    # Get recommendations for each movie
    all_recommendations = {}
    for movie in movie_list:
        similar_movies = find_similar_movies_svd(movie, n_recommendations=10)
        for i, rec_movie in enumerate(similar_movies):
            # Calculate score based on position (inverse of index)
            score = 10 - i  # Higher score for movies appearing earlier in the list
            if rec_movie in all_recommendations:
                all_recommendations[rec_movie] += score
            else:
                all_recommendations[rec_movie] = score
    
    # Remove input movies from recommendations if they appear
    for movie in movie_list:
        if movie in all_recommendations:
            del all_recommendations[movie]
    
    # Sort by total score
    sorted_recommendations = sorted(all_recommendations.items(), 
                                  key=lambda x: x[1], 
                                  reverse=True)
    
    # Return top N recommendations
    return [movie for movie, score in sorted_recommendations[:n_recommendations]]

# Example usage:
# movie_list = ["Toy Story (1995)", "The Matrix (1999)", "Jurassic Park (1993)"]
# recommendations = recommend_for_multiple_users_svd(movie_list)

# Test with input sets
# input_sets = {
#     "2_movies": ["The Princess Diaries (2001)", "Hannah Montana: The Movie (2009)"],
#     "5_movies": ["Fight Club (1999)", "The Princess Diaries (2001)", "Hannah Montana: The Movie (2009)", "The Other Woman (2014)", "Just Friends (2005)"],
#     "10_movies": ["The Princess Diaries (2001)", "Hannah Montana: The Movie (2009)", "The Other Woman (2014)", "Just Friends (2005)", "Fight Club (1999)", 
#                   "Titanic (1997)", "Friends with Benefits (2011)", "The Pink Panther (2006)", "The Addams Family (1991)", "Father of the Bride (1950)"]
# }

# for test_name, movies in input_sets.items():
#     print(f"\nResults for {test_name}:")
#     recommendations = recommend_for_multiple_movies(movies)
#     for movie in recommendations:
#         print(f"- {movie}")
