from flask import Flask, render_template, request, jsonify
from logic import recommend_for_two_users_with_five_results, get_movie_poster_tmdb
from logic_svd import recommend_for_two_users_with_five_results_svd
import pandas as pd

app = Flask(__name__)

# Load your dataset and model
df = pd.read_csv("data/movies3.csv")

# Define your recommendation logic
def recommend_movies(user_input):
    # Example logic, replace with your actual logic
    recommendations = df.sample(5)['movie_title'].tolist()
    return recommendations

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/search_movies", methods=["GET"])
def search_movies():
    query = request.args.get("query", "").lower()
    if not query:
        return jsonify([])  # Return empty list if no query
    matching_movies = df[df["title"].str.lower().str.contains(query)].head(10)  # Limit results
    suggestions = matching_movies["title"].tolist()
    return jsonify(suggestions)

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.json.get('user_input')  # Fetch input from the frontend
    recommendations = recommend_movies(user_input)
    return jsonify(recommendations)

# route for generating a random movie selection
@app.route('/random_movie', methods=['GET'])
def random_movie():
    random_movie = df.sample(n=1).iloc[0]['title']  # column is named 'title'
    random_movie_url = get_movie_poster_tmdb(random_movie);
    return jsonify({'movie': random_movie,'poster_url':random_movie_url})

# route for getting recommandations from logic file
@app.route('/get_movie_results', methods=['POST'])
def get_movie_results():
    data = request.json  # Expect JSON input
    movie1 = data.get("movie1")
    movie2 = data.get("movie2")
    
    if not movie1 or not movie2:
        return jsonify({"error": "Both movies are required"}), 400

    # Call the Python function
    results = recommend_for_two_users_with_five_results_svd(movie1, movie2)
    print(results)
    
    #ADDED
    # Include posters for each recommendation
    recommendations_with_posters_and_summary = []
    for movie in results:
        poster_url, summary = get_movie_poster_tmdb(movie)  # Fetch poster URL
        recommendations_with_posters_and_summary.append({
            "title": movie,
            "poster_url": poster_url if poster_url else "https://via.placeholder.com/500",
            "summary": summary if summary else "No summary available."
        })

    # Return the results as JSON
    return jsonify(recommendations_with_posters_and_summary)

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