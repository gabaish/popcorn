document.addEventListener("DOMContentLoaded", () => {
    // Set up movie input fields with suggestions
    setupMovieInput({
        inputId: "your-movie-input",
        suggestionsId: "your-movie-suggestions",
        placeholderId: "your-placeholder",
    });

    setupMovieInput({
        inputId: "their-movie-input",
        suggestionsId: "their-movie-suggestions",
        placeholderId: "their-placeholder",
    });

    // Sets up the movie input field to display suggestions as the user types
    function setupMovieInput({ inputId, suggestionsId, placeholderId }) {
        const movieInput = document.getElementById(inputId);
        const suggestionsList = document.getElementById(suggestionsId);
        const moviePlaceholder = document.getElementById(placeholderId);

        // Fetches movie suggestions based on the query entered by the user
        async function fetchSuggestions(query) {
            const response = await fetch(`/search_movies?query=${query}`);
            return await response.json();
        }

        // Listen for user input and fetch suggestions dynamically
        movieInput.addEventListener("input", async () => {
            const query = movieInput.value.trim();
            if (!query) {
                suggestionsList.classList.add("hidden");
                return;
            }

            const suggestions = await fetchSuggestions(query);
            suggestionsList.innerHTML = "";

            if (suggestions.length > 0) {
                suggestions.forEach((movie) => {
                    const listItem = document.createElement("li");
                    listItem.textContent = movie;
                    
                    // Handle movie selection and poster display
                    listItem.addEventListener("click", async () => {
                        try {
                            movieInput.value = movie;
                            moviePlaceholder.textContent = "";
                            suggestionsList.classList.add("hidden");
                    
                            // Fetch the movie poster
                            const response = await fetch(`/get_movie_poster?title=${encodeURIComponent(movie)}`);
                            if (!response.ok) {
                                throw new Error('Failed to fetch movie poster');
                            }
                            const data = await response.json();
                            if (data.error) {
                                throw new Error(data.error);
                            }
                    
                            // Add or update the movie image
                            const pickCard = movieInput.closest('.pick-card');
                            const movieImage = pickCard.querySelector('.movie-image');
                            if (movieImage) {
                                movieImage.src = data.poster_url;
                                movieImage.alt = movie;
                                movieImage.style.display = 'block'; // Make the image visible
                            } else {
                                const img = document.createElement('img');
                                img.src = data.poster_url;
                                img.alt = movie;
                                img.classList.add('movie-image');
                                img.style.display = 'block'; // Ensure the new image is visible
                                pickCard.appendChild(img);
                            }
                        } catch (error) {
                            console.error('Error fetching movie poster:', error);
                            alert('Could not fetch the movie poster. Please try again.');
                        }
                    });

                    suggestionsList.appendChild(listItem);
                });

                suggestionsList.classList.remove("hidden");
            } else {
                suggestionsList.classList.add("hidden");
            }
        });

        document.addEventListener("click", (e) => {
            if (!movieInput.contains(e.target) && !suggestionsList.contains(e.target)) {
                suggestionsList.classList.add("hidden");
            }
        });
    }

    // Set up dice buttons for random movies
    const diceButtons = document.querySelectorAll(".dice-button");
    diceButtons.forEach((button) => {
        button.addEventListener("click", async () => {
            try {
                const response = await fetch('/random_movie');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                
                // Get the parent pick-card element
                const pickCard = button.closest('.pick-card');
                if (!pickCard) {
                    throw new Error('Could not find parent pick-card');
                }
                
                // Find the placeholder element within this pick-card
                const placeholder = pickCard.querySelector('.movie-placeholder p');
                if (!placeholder) {
                    throw new Error('Could not find placeholder element');
                }
                
                // Update the placeholder text
                placeholder.textContent = "";
                
                // update the input field in this pick-card
                const input = pickCard.querySelector('input[type="text"]');
                if (input) {
                    input.value = data.movie;
                }

                // Add or update the movie image
                const movieImage = pickCard.querySelector('.movie-image');
                movieImage.src = data.poster_url[0];
                movieImage.alt = data.movie;
                movieImage.style.display = 'block'; 

            } catch (error) {
                console.error('Error fetching random movie:', error);
                alert('Could not fetch a random movie. Please try again.');
            }
        });
    });

    // Get all required elements for next functions
    const knnCarouselContainer = document.getElementById("knn-results");
    const svdCarouselContainer = document.getElementById("svd-results");
    const resultsContainer = document.querySelector(".results-container");
    const summaryContainer = document.getElementById("movie-summary");
    const carouselContent = document.querySelector(".carousel-content");
    const knnScrollLeftButton = document.getElementById("knn-scroll-left");
    const knnScrollRightButton = document.getElementById("knn-scroll-right");
    const svdScrollLeftButton = document.getElementById("svd-scroll-left");
    const svdScrollRightButton = document.getElementById("svd-scroll-right");
    const loadingIndicator = document.querySelector(".loading-indicator");


    // Add scroll button functionality for knn
    if (knnScrollLeftButton && knnScrollRightButton) {
        knnScrollLeftButton.addEventListener("click", () => {
            knnCarouselContainer.scrollBy({
                left: -200,
                behavior: "smooth"
            });
        });

        knnScrollRightButton.addEventListener("click", () => {
            knnCarouselContainer.scrollBy({
                left: 200,
                behavior: "smooth"
            });
        });
    }

    // Add scroll button functionality for svd
    if (svdScrollLeftButton && svdScrollRightButton) {
        svdScrollLeftButton.addEventListener("click", () => {
            svdCarouselContainer.scrollBy({
                left: -200,
                behavior: "smooth"
            });
        });

        svdScrollRightButton.addEventListener("click", () => {
            svdCarouselContainer.scrollBy({
                left: 200,
                behavior: "smooth"
            });
        });
    }

    // Fetches movie recommendations and displays them in the results container
    async function fetchResults() {
        try {
            const movie1 = document.getElementById("your-movie-input").value;
            const movie2 = document.getElementById("their-movie-input").value;
    
            if (!movie1 || !movie2) {
                alert("Please select both movies first!");
                return;
            }

            resultsContainer.style.display = "none";
            loadingIndicator.style.display = "block";
            carouselContent.style.display = "none";
            summaryContainer.classList.remove('visible');
            summaryContainer.style.display = "none";

            const knnContainer = document.getElementById("knn-results");
            const svdContainer = document.getElementById("svd-results");
    
            knnContainer.innerHTML = "";
            svdContainer.innerHTML = "";
            summaryContainer.innerHTML = `<p>Summary will appear here when you click a poster.</p>`;
    
            const response = await fetch("/get_movie_results", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ movie1, movie2 }),
            });
    
            const data = await response.json();
    
            // Populate KNN results
            data.knn.forEach((movie) => {
                const card = createMovieCard(movie);
                knnContainer.appendChild(card);
            });
    
            // Populate SVD results
            data.svd.forEach((movie) => {
                const card = createMovieCard(movie);
                svdContainer.appendChild(card);
            });

            showResultsContainer();
        } catch (error) {
            console.error("Error fetching results:", error);
        }
    }
    
    // Creates a card for displaying a movie with its poster and summary
    function createMovieCard(movie) {
        const card = document.createElement("div");
        card.classList.add("result-card");
    
        card.innerHTML = movie.poster_url
            ? `<img src="${movie.poster_url}" alt="${movie.title}">`
            : `<div class="movie-title">${movie.title}</div>`;
    
        // Display movie summary on card click
        card.addEventListener("click", () => {
            const summaryContainer = document.getElementById("movie-summary");
            summaryContainer.innerHTML = `<h2>${movie.title}</h2><p>${movie.summary}</p>`;
            summaryContainer.style.display = "block";
        });
    
        return card;
    }

    // Displays the results container and associated elements
    function showResultsContainer() {
        loadingIndicator.style.display = "none";
        carouselContent.style.display = "flex";
        summaryContainer.classList.add('visible');
        summaryContainer.style.display = "block";
        const resultsContainer = document.querySelector('.results-container');
        if (resultsContainer) {
            resultsContainer.style.display = 'flex';
        }
        if (svdScrollLeftButton) svdScrollLeftButton.style.display = 'block';
        if (svdScrollRightButton) svdScrollRightButton.style.display = 'block';
        if (knnScrollLeftButton) knnScrollLeftButton.style.display = 'block';
        if (knnScrollRightButton) knnScrollRightButton.style.display = 'block';
    }

// Attach click handler to shuffle button
const shuffleButton = document.querySelector(".shuffle-button");
if (shuffleButton) {
    shuffleButton.addEventListener("click", fetchResults);
} else {
    console.error("Error: Shuffle button not found!");
}
});