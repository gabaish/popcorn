import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
import requests
import re

# TMDb API configuration
TMDB_API_KEY = "f9c68fee291e011281ee8722f40fbc18" 
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

# Load datasets
movies2 = pd.read_csv('data/movies3.csv')
ratings = pd.read_csv('data/ratings.csv')

# Merge movie and rating datasets
merged_data = pd.merge(ratings, movies2, on='movieId')


# Create a sparse matrix of users and movies for recommendation modeling
row = merged_data['userId'].astype('category').cat.codes  # Unique user IDs as matrix rows
col = merged_data['title'].astype('category').cat.codes  # Unique movie titles as matrix columns
data = merged_data['rating'].values   # Ratings as matrix data
user_movie_sparse = csr_matrix((data, (row, col))) # Sparse matrix representation


# Mapping movie titles to their corresponding columns in the sparse matrix
title_to_index = dict(enumerate(merged_data['title'].astype('category').cat.categories))
index_to_title = {v: k for k, v in title_to_index.items()}

# Build Nearest Neighbors model
# Computing movie similarity based on user ratings
model = NearestNeighbors(metric='cosine', algorithm='brute')
model.fit(user_movie_sparse.T)  # Transpose: rows represent movies, columns represent users

# Recommend similar movies based on the given movie title using Nearest Neighbors
def recommend_movies_by_title_nn(movie_title, model, user_movie_sparse, top_n=5):
    """Recommend similar movies based on the given movie title."""
    if movie_title not in index_to_title:
        return f"Movie '{movie_title}' not found."

    # Get the index of the movie in the sparse matrix
    movie_idx = index_to_title[movie_title]

    # Find the nearest neighbors (most similar movies)
    distances, indices = model.kneighbors(user_movie_sparse.T[movie_idx], n_neighbors=top_n + 1)

    # Return the top N similar movies
    similar_movies = [(title_to_index[i], distances[0][j]) for j, i in enumerate(indices[0]) if i != movie_idx]
    return similar_movies[:top_n]

def recommend_for_two_users_with_five_results(user1_movie, user2_movie):
    """Recommend movies for two users with guaranteed 5 results."""
    top_n = 5  # Number of recommendations
    # Recommendations for User 1
    user1_recommendations = recommend_movies_by_title_nn(user1_movie, model, user_movie_sparse, top_n * 2)

    # Recommendations for User 2
    user2_recommendations = recommend_movies_by_title_nn(user2_movie, model, user_movie_sparse, top_n * 2)

    user1_recommendations_set = set([rec[0] for rec in user1_recommendations])
    user2_recommendations_set = set([rec[0] for rec in user2_recommendations])

    # Check for common recommendations between the two users
    common_recommendations = user1_recommendations_set.intersection(user2_recommendations_set)

    # If there are >= 5 recommendations
    if len(common_recommendations) >= top_n:
        return list(common_recommendations)[:top_n]

    # Rank all their recommended movies based on combined similarity scores
    combined_scores = {}
    for movie, dist in user1_recommendations:
        combined_scores[movie] = 1 - dist

    for movie, dist in user2_recommendations:
        combined_scores[movie] = combined_scores.get(movie, 0) + (1 - dist)

    # Return top 5 recommendations
    ranked_recommendations = sorted(combined_scores, key=combined_scores.get, reverse=True)
    recommendations = ranked_recommendations[:top_n]
    print("Top 5 KNN recommendations:", recommendations)
    return recommendations

# Normalize movie titles by removing articles and years
def normalize_title(title):
    # Remove year in parentheses (e.g., "Pulp Fiction (1994)" -> "Pulp Fiction")
    clean_title = re.sub(r"\s\(\d{4}\)$", "", title)
    
    # Remove leading articles ("The", "A", "An")
    clean_title = re.sub(r"^(The|A|An)\s", "", clean_title, flags=re.IGNORECASE)
    
    return clean_title.strip()

# Fetch the poster URL and summary for a given movie title using TMDb API
def get_movie_poster_tmdb(title):
    match = re.search(r"\((\d{4})\)$", title)
    year = match.group(1) if match else None
    clean_title = normalize_title(title)

    queries = [
        {"query": title, "year": year},          # Original title with year
        {"query": clean_title, "year": year},   # Normalized title with year
        {"query": title},                       # Original title without year
        {"query": clean_title}                  # Normalized title without year
    ]
    
    for params in queries:
        # Make the API request
        params['api_key'] = TMDB_API_KEY
        search_url = f"{TMDB_BASE_URL}/search/movie"
        response = requests.get(search_url, params=params)
        data = response.json()
        
        if response.status_code == 200 and data['results']:
            # Get the first result's poster path
            result = data['results'][0]
            poster_path = result.get('poster_path')
            summary = result.get('overview', 'No summary available.')
            poster_url = (
                f"https://image.tmdb.org/t/p/w500{poster_path}" 
                if poster_path 
                else None
            )

            return poster_url, summary
    return None,'No summary available'  # No poster found

# Display movie posters for a list of recommended titles
def display_movie_posters_tmdb(recommended_titles):
    for title in recommended_titles:
        poster_url = get_movie_poster_tmdb(title)
        if poster_url:
            display(Image(url=poster_url, width=200))
        else:
            print(f"No poster found for '{title}'.")


# Example usage (uncomment to run):
# user1_movie = "Toy Story (1995)"
# user2_movie = "Forrest Gump (1994)"
# recommendations = recommend_for_two_users_with_five_results(user1_movie, user2_movie)
# print("Top 5 Recommendations for Both Users:")
# print(recommendations)
# display_movie_posters_tmdb(recommendations)