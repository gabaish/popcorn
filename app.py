from flask import Flask, render_template, request, jsonify
from logic import recommend_for_two_users_with_five_results
import pandas as pd

app = Flask(__name__)

# Load your dataset and model
df = pd.read_csv("data/movies.csv")

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
    random_movie = df.sample(n=1).iloc[0]['title']  # Assuming the column is named 'title'
    return jsonify({'movie': random_movie})

# route for getting recommandations from logic file
@app.route('/get_movie_results', methods=['POST'])
def get_movie_results():
    data = request.json  # Expect JSON input
    movie1 = data.get("movie1")
    movie2 = data.get("movie2")
    
    if not movie1 or not movie2:
        return jsonify({"error": "Both movies are required"}), 400

    # Call the Python function
    results = recommend_for_two_users_with_five_results(movie1, movie2)
    print(results)
    
    # Return the results as JSON
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
