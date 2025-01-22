# Popcorn

![](media/image1.png)

## Introduction

### What is Popcorn?

Popcorn is a movie recommendation system designed to help users find movies for their movie nights based on collaborative preferences. The system combines modern web technologies with machine learning techniques, including **Nearest Neighbors (KNN)** and **Singular Value Decomposition (SVD),** to generate personalized movie suggestions that appeal to multiple viewers' tastes. By combining insights from historical user preferences with real-time data from external APIs, Popcorn enhances the movie selection process, making it both efficient and enjoyable.

### What is the Movie Night Dilemma?

The Movie Night Dilemma is a common social challenge that emerges when friends, couples, or families attempt to select a film that satisfies everyone's tastes. Unlike traditional recommendation systems that focus on individual users, the challenge here lies in finding a middle ground between different, often conflicting, viewing preferences. Consider a couple planning their date night - one person might enjoy intense psychological thrillers while their partner prefers lighthearted comedies. Existing streaming platforms typically focus on single-user recommendations, leaving the challenge of reconciling diverse tastes unaddressed.

![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](./static/popcorn_no_background.png)![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image2.png)![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image2.png)![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image2.png)

## The Problem

1. **Diverse Preferences:**
   Different users often have contrasting movie preferences, making it difficult to agree on a single movie. For example, one person might prefer high-action blockbusters, while another enjoys thought-provoking dramas or comedies.

2. **Lack of Group-Focused Solutions:**
   Existing streaming platforms and recommendation systems are designed for individual users and do not offer a collaborative way to recommend movies for multiple people.

3. **Information Overload:**
   With thousands of movies available across various streaming platforms, users can easily become overwhelmed when trying to choose.

4. **Limited Contextual Information:**
   Users often lack quick access to essential information like posters, summaries, or trailers, making it harder to finalize a decision.

The goal of this project is to develop a group-focused movie recommendation system that analyzes preferences from multiple users, suggests movies that are likely to appeal to all participants, provides additional contextual information (e.g., posters, summaries) to enhance the selection process, and solves the Movie Night Dilemma by reducing the friction in group decision-making and transforming it into a seamless, enjoyable experience.

![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image2.png)![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image2.png)![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image2.png)![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image2.png)

## Solution -- Collaborative Filtering

### Overview

Popcorn's solution involves using a collaborative filtering approach to analyze historical user preferences and find common ground between two users.

The system uses K-Nearest Neighbors (KNN) and Singular Value Decomposition (SVD) to recommend movies based on similarity scores.

### Key Components

- **User-Movie Matrix**: A sparse matrix representing user ratings for various movies.
- **Nearest Neighbors Model**: A KNN model trained on the user-movie matrix to find similar movies.
- **SVD Model**: A SVD model trained on the user-movie matrix to find similar movies.
- **TMDb API Integration**: Real-time data fetching for movie posters and summaries.

### Usage

The backend processes inputs from both users and generates five movie recommendations that are most likely to be enjoyed by both parties.

Recommendations are generated by both models, allowing for a direct comparison of their performance.

Each recommendation includes a poster and a brief summary fetched from the TMDb API.

![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image2.png)![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image2.png)![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image2.png)![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image2.png)

## Technical Implementation

### Data collecting and Processing

Popcorn uses two data sets:

- **Movies Dataset**: A CSV file containing movie titles and metadata.
- **Ratings Dataset**: A CSC file with user ratings for various movies.

The datasets are merged to create a user-movie rating matrix. Sparse representations of the matrix are used to improve computational efficiency.

The datasets, sourced from Kaggle, ensure reliability and quality for our analysis.

### Recommendation Algorithms

The recommendation engine is built using two powerful algorithms: **K-Nearest Neighbours (KNN)** and **Singular Value Decomposition (SVD).**

### Collaborative Filtering

Collaborative filtering works by analyzing patterns in user behaviour, such as movie ratings, to recommend content. Instead of relying on explicit metadata about movies (e.g., genre or director), it focuses on user interactions to uncover hidden relationships between items and users.

### K-Nearest Neighbours (KNN)

The KNN algorithm is used for item-based collaborative filtering in this recommendation system. Here's how it works:

1. **Finding Neighbours:**
   - Given a specific movie as input, the algorithm calculates its similarity to all other movies in the dataset. This similarity is measured using cosine similarity.
   - The algorithm then selects the topmost similar movies, known as the "neighbours."

2. **Generating Recommendations:**
   - When two input movies are provided, the system finds the top neighbours for each movie independently.
   - A combined list of recommendations is created by merging the two sets of neighbours, ensuring at least 5 unique and highly relevant results.

3. **Key Functions:**
   - **Recommend_movies_by_title_nn**: Identifies movies most similar to a given title using the KNN model.
   - **Recommend_for_two_users_with_five_results**: Combines recommendations for two users or input movies, guaranteeing at least five unique recommendations for a more diverse result set.

### Singular Value Decomposition (SVD)

SVD is a matrix factorization technique widely used in recommendation systems, particularly for collaborative filtering. It works by decomposing the user-item interaction matrix into three smaller matrices:

1. **User Matrix (U):** Represents the relationship between users and latent factors.
2. **Singular Values (Σ):** Captures the strength of each latent factor.
3. **Item Matrix (V^T):** Represents the relationship between items (movies) and latent factors.

The decomposition allows us to project both users and items into a shared latent feature space, enabling the system to predict ratings for unseen movies by calculating the dot product of the corresponding user and item vectors.

### What Are Latent Features?

Latent features are hidden factors that capture underlying patterns in the data. For example, in the context of movies, latent features might represent abstract concepts like "genre preference," "movie popularity," or "actor influence." These features are not explicitly labelled but are inferred from the data during matrix factorization.

### How SVD Generates Recommendations:

1. **Decomposing the Matrix:**
   - The original user-item matrix (containing user ratings) is factorized into the U, Σ, and V^T matrices.
   - This step identifies latent factors that capture hidden relationships between users and movies.

2. **Predicting Ratings:**
   - For a given user and a specific movie, the system calculates a predicted rating using the reconstructed user-item matrix derived from the factorized components.

3. **Ranking Recommendations:**
   - Movies with the highest predicted ratings for a user are recommended. These movies are ranked based on their scores.

4. **Key Functions for SVD:**
   - find_similar_movies_svd: Identifies movies similar to a given title based on latent features.
   - recommend_for_two_users_with_five_results_svd: Combines recommendations for two input movies, ensuring a diverse list of at least five unique results.

![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image2.png)![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image2.png)![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image2.png)![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image2.png)

## Frontend Integration

The web interface is built using HTML, CSS, and JavaScript. Flask is used as the background framework to handle API requests and serve the frontend.

- Movie Input: Users enter movie names, and suggestions are fetched dynamically.
- Recommendation Display: Recommended movies are displayed as a carousel with posters and summaries.

We provide separate recommendations for both models.

- Random Movie Generator: a dice button allows the users to get random movies suggestions.

![](media/image3.png)

![results for the SVD and KNN algorithms.](media/image4.png)

![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image2.png)![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image2.png)![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image2.png)![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image2.png)

# Experiments and Results

## Experiment 1 -- KNN model with varied number of inputs

The goal of this experiment was to evaluate how KNN model performs when given different numbers of input movies. Specifically, we tested the system with:

- 2 movies input: ["The Princess Diaries (2001)", "Hannah Montana: The Movie (2009)"]
- 5 movies input: ["The Princess Diaries (2001)", "Hannah Montana: The Movie (2009)", "The Other Woman (2014)", "Just Friends (2005)", "Fight Club (1999)"]
- 10 movies input: ["The Princess Diaries (2001)", "Hannah Montana: The Movie (2009)", "The Other Woman (2014)", "Just Friends (2005)", "Fight Club (1999)", "Titanic (1997)", "Friends with Benefits (2011)", "The Pink Panther (2006)", "The Addams Family (1991)", "Father of the Bride (1950)"]

### Results and Observations

#### For 2 Input Movies:
Recommendations:
- The Princess Diaries 2: Royal Engagement (2004)
- Legally Blonde (2001)
- Freaky Friday (2003)
- Camp Rock (2008)
- How to Lose a Guy in 10 Days (2003)

Observation:
The recommendations were primarily focused on lighthearted family comedies and dramas, closely matching the genres of the input movies. This shows that the system successfully identified relevant movies based on genre and tone.

#### For 5 Input Movies:
Recommendations:
- The Matrix (1999)
- Memento (2000)
- American Beauty (1999)
- The Lord of the Rings: The Fellowship of the Ring (2001)
- Pulp Fiction (1994)

Observation:
The recommendations shifted to a mix of action, thrillers, and classic dramas, reflecting the increased diversity of genres in the input set. This demonstrates that the system adapts well to varied input by providing a broader range of recommendations.

#### For 10 Input Movies:
Recommendations:
- The Matrix (1999)
- Just Go with It (2011)
- The Proposal (2009)
- We're the Millers (2013)
- The Ugly Truth (2009)

Observation:
Despite the larger and more diverse input set, the system provided a relatively focused set of romantic comedies and lighthearted movies. This suggests that movies with overlapping genres or themes received higher cumulative similarity scores, dominating the results.

Based on the results, the following improvements could enhance the recommendation system:

1. **Introduce diversity constraints**: Prevent domination by a single genre in larger input sets by enforcing a minimum level of diversity in the recommendations.
2. **Incorporate genre balancing**: Implement a mechanism that balances recommendations across genres when input sets are large and diverse.

## Experiment 2 -- SVD Model with Varied Number of Inputs

The goal of this experiment was to evaluate how the SVD-based recommendation system performs when given different numbers of input movies. Specifically, we tested the system with the following input sets (same input sets we used in the KNN experiment):

- **2 movies input:** ["The Princess Diaries (2001)", "Hannah Montana: The Movie (2009)"]
- **5 movies input:** ["The Princess Diaries (2001)", "Hannah Montana: The Movie (2009)", "The Other Woman (2014)", "Just Friends (2005)", "Fight Club (1999)"]
- **10 movies input:** ["The Princess Diaries (2001)", "Hannah Montana: The Movie (2009)", "The Other Woman (2014)", "Just Friends (2005)", "Fight Club (1999)", "Titanic (1997)", "Friends with Benefits (2011)", "The Pink Panther (2006)", "The Addams Family (1991)", "Father of the Bride (1950)"]

### Results and Observations

#### For 2 Input Movies:

Recommendations:
- 10 Things I Hate About You (1999)
- The Devil Wears Prada (2006)
- How to Lose a Guy in 10 Days (2003)
- The Proposal (2009)
- Miss Congeniality (2000)

Observation:
The recommendations largely consisted of romantic comedies and light-hearted dramas, closely aligning with the tone and genre of the input movies. This indicates that the SVD model successfully captured the latent features of the input movies and provided relevant recommendations based on genre similarity.

#### For 5 Input Movies:

Recommendations:
- 10 Things I Hate About You (1999)
- The Proposal (2009)
- How to Lose a Guy in 10 Days (2003)
- The Devil Wears Prada (2006)
- Mean Girls (2004)

Observation:
With more diverse input movies, the recommendations still leaned heavily toward romantic comedies and teen dramas. While the system provided consistent results with high relevance, it showed limited adaptability to the broader range of genres present in the input.

#### For 10 Input Movies:

Recommendations:
- 10 Things I Hate About You (1999)
- The Proposal (2009)
- Easy A (2010)
- How to Lose a Guy in 10 Days (2003)
- The Devil Wears Prada (2006)

Observation:
Despite the significantly larger and more varied input set, the recommendations remained focused on romantic comedies and teen-focused movies. This suggests that movies with overlapping genres and themes received higher cumulative similarity scores, dominating the results and limiting the diversity of recommendations.

### Suggested Improvements for the SVD Model

1. **Implement Diversity Constraints:** Prevent the system from overly favoring specific genres or themes, particularly when dealing with larger input sets. This could involve enforcing a minimum representation of underrepresented genres.
2. **Adjust Similarity Aggregation:** Experiment with weighting strategies to give equal importance to all input movies, ensuring that less dominant genres contribute meaningfully to the final recommendations.

## Experiment 3 -- KNN and SVD models comparison on 2 movies

The goal of this experiment was to directly compare the recommendations generated by KNN and SVD for pairs of input movies, observing their behavior in producing personalized suggestions.

Five pairs of movies were selected to evaluate the models:

1. Toy Story (1995) & The Amazing Spider-Man (2012)
2. Notting Hill (1999) & Crazy Rich Asians (2018)
3. Monte Carlo (2011) & Scary Movie (2000)
4. Mission: Impossible - Fallout (2018) & The Equalizer 2 (2018)
5. The Transporter (2002) & Blended (2014)

### Results and observations:

| SVD Recommendations | KNN Recommendations | Chosen Movies |
|-------------------|-------------------|--------------|
| Toy Story 2<br>X-Men: First Class<br>Aladdin<br>Iron Man 2<br>Captain America: The First Avenger | Star Wars: Episode IV - A New Hope<br>Toy Story 2<br>Amazing Spider-Man 2<br>Back to the Future<br>Forrest Gump | Toy Story (1995)<br>The Amazing Spider-Man (2012) |
| Pretty Woman<br>Thor: Ragnarok<br>Four Weddings and a Funeral<br>Guardians of the Galaxy 2<br>Sleepless in Seattle | You've Got Mail<br>Bridget Jones's Diary<br>My Best Friend's Wedding<br>Shakespeare in Love<br>Erin Brockovich | Notting Hill (1999)<br>Crazy Rich Asians (2018) |
| Proposal<br>Meet the Parents<br>10 Things I Hate About You<br>American Pie<br>American Pie 2 | Scary Movie 2<br>Scary Movie 3<br>American Pie 2<br>Me, Myself & Irene<br>Road Trip | Monte Carlo (2011)<br>Scary Movie (2000) |
| Guardians of the Galaxy 2<br>Untitled Spider-Man Reboot<br>Deadpool 2<br>Thor: Ragnarok<br>Rogue One: A Star Wars Story | Venom<br>Ant-Man and the Wasp<br>Black Panther<br>Ready Player One<br>Avengers: Infinity War - Part I | Mission: Impossible - Fallout (2018)<br>The Equalizer 2 (2018) |
| Easy A<br>Bourne Supremacy<br>Notebook<br>Transporter<br>We're the Millers | Transporter 2<br>Transporter 3<br>Crank<br>xXx<br>Fast and the Furious | The Transporter (2002)<br>Blended (2014) |

**The KNN** model displayed strong emphasis on maintaining genre consistency and familiar connections. For example:

- With input movies such as *Toy Story (1995)* and *The Amazing Spider-Man (2012)*, the model recommended direct sequels like *Toy Story 2* and *Amazing Spider-Man 2*, alongside timeless classics like *Star Wars: Episode IV - A New Hope* and *Back to the Future*.
- Similarly, for the pair *Notting Hill (1999)* and *Crazy Rich Asians (2018)*, the recommendations included well-known romantic comedies like *You've Got Mail*, *Bridget Jones's Diary*, and *My Best Friend's Wedding*.

This behavior demonstrates KNN's ability to effectively identify and suggest closely related movies based on explicit similarity metrics. However, its reliance on direct matches sometimes limited recommendation variety. This was evident in the case of *Scary Movie (2000)* and *Monte Carlo (2011)*, where the suggestions largely consisted of sequels and similar comedy titles, such as *Scary Movie 2* and *Scary Movie 3*.

**The SVD** model took a different approach, leveraging latent feature extraction to produce more varied and sometimes unexpected recommendations. For instance:

- When given *Toy Story (1995)* and *The Amazing Spider-Man (2012)* as inputs, SVD suggested movies such as *X-Men: First Class* and *Aladdin*. Although these choices moved away from direct sequels, they remained aligned with the broader themes of family entertainment and action-adventure.
- For *Notting Hill (1999)* and *Crazy Rich Asians (2018)*, SVD's recommendations included *Pretty Woman* and *Thor: Ragnarok*, illustrating its ability to infer nuanced connections within user preferences based on latent patterns.

Despite the diversity in its recommendations, SVD occasionally generated results that did not closely align with the tone or genre of the input movies. For example, *Thor: Ragnarok* appearing in the romantic comedy context highlights the model's exploratory nature, which, while innovative, can sometimes lead to mismatched suggestions.

### Suggested Improvements:

Combining their strengths in a hybrid system could deliver an optimal recommendation experience, balancing familiarity with variety for group-based movie suggestions.

![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image1.png)![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image1.png)![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image1.png)![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image1.png)

## Conclusions

- Popcorn successfully addresses the "Movie Night Dilemma" by providing a recommendation system tailored for groups. By combining collaborative filtering techniques with an intuitive interface, it offers a unique solution that enhances the movie selection experience.
- Based on the conducted experiments, we believe that SVD model results better movie recommendations for 2 movies input, while KNN model results better movie recommendations for larger inputs.

### Future enhancements could include:

- Adding UI support for more than two users
- Incorporating additional filtering options (e.g., genre, release year)
- Expanding the database to include more movie metadata
- Create a hybrid system based on both SVD and KNN models

![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image1.png)![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image1.png)![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image1.png)![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image1.png)

## Installation and Running Instructions

### Prerequisites

- Python 3.8+
- Flask
- Required Python libraries

### Installation Steps

1. Clone the Repository:
```bash
git clone https://github.com/your-repo/popcorn
```

2. Run the Application:
```bash
python app.py
```

3. Access the Web Interface:
Open a web browser and go to http://127.0.0.1:5000.

![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image1.png)![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image1.png)![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image1.png)![A bucket of popcorn and 3d glasses AI-generated content may be incorrect.](media/image1.png)
