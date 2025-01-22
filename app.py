from flask import Flask, render_template, request, jsonify
from logic_knn import recommend_for_two_users_with_five_results, get_movie_poster_tmdb
from logic_svd import recommend_for_two_users_with_five_results_svd
import pandas as pd

app = Flask(__name__)

# Load your dataset and model
df = pd.read_csv("data/movies3.csv")

# Render the home page of the application
@app.route('/')
def home():
    return render_template('index.html')

# Handle search queries for movie titles
@app.route("/search_movies", methods=["GET"])
def search_movies():
    query = request.args.get("query", "").lower()
    if not query:
        return jsonify([])  # Return empty list if no query
    matching_movies = df[df["title"].str.lower().str.contains(query)].head(10)  # Filter matching titles
    suggestions = matching_movies["title"].tolist() # Extract the titles as a list
    return jsonify(suggestions)

# Select a random movie from the dataset and fetch its poster URL
@app.route('/random_movie', methods=['GET'])
def random_movie():
    random_movie = df.sample(n=1).iloc[0]['title']  # column is named 'title'
    random_movie_url = get_movie_poster_tmdb(random_movie);
    return jsonify({'movie': random_movie,'poster_url':random_movie_url})

# Generate movie recommendations using KNN and SVD models for two selected movies
@app.route('/get_movie_results', methods=['POST'])
def get_movie_results():
    data = request.json
    movie1 = data.get("movie1")
    movie2 = data.get("movie2")
    
    if not movie1 or not movie2:
        return jsonify({"error": "Both movies are required"}), 400

    # Fetch recommendations  from both models
    knn_results = recommend_for_two_users_with_five_results(movie1, movie2)
    svd_results = recommend_for_two_users_with_five_results_svd(movie1, movie2)

    # Prepare KNN recommendations with posters and summaries
    knn_recommendations = []
    for movie in knn_results:
        poster_url, summary = get_movie_poster_tmdb(movie)
        knn_recommendations.append({
            "title": movie,
            "poster_url": poster_url if poster_url else "https://via.placeholder.com/500",
            "summary": summary if summary else "No summary available."
        })

    # Prepare SVD recommendations with posters and summaries
    svd_recommendations = []
    for movie in svd_results:
        poster_url, summary = get_movie_poster_tmdb(movie)
        svd_recommendations.append({
            "title": movie,
            "poster_url": poster_url if poster_url else "https://via.placeholder.com/500",
            "summary": summary if summary else "No summary available."
        })

    return jsonify({
        "knn": knn_recommendations,
        "svd": svd_recommendations
    })

# Fetch the poster URL for a given movie title
@app.route('/get_movie_poster', methods=['GET'])
def get_movie_poster():
    movie_name = request.args.get('title')
    if not movie_name:
        return jsonify({'error': 'Movie title is required'}), 400
    
    try:
        poster_url = get_movie_poster_tmdb(movie_name)
        if not poster_url:
            return jsonify({'error': 'Poster not found'}), 404
        return jsonify({'poster_url': poster_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)