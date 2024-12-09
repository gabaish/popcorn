// Wait until the DOM is fully loaded
document.addEventListener("DOMContentLoaded", () => {
    // Reference to the results container
    const resultsContainer = document.getElementById("results");

    // Example function: Show the results section when a button is clicked
    const shuffleButton = document.querySelector(".shuffle-button");
    shuffleButton.addEventListener("click", () => {
        // Remove the hidden class to display results
        resultsContainer.classList.remove("hidden");
    });

    // Example: Add behavior for the "Pick your movie" buttons
    const pickButtons = document.querySelectorAll(".pick-button");
    pickButtons.forEach((button) => {
        button.addEventListener("click", () => {
            alert("Pick movie functionality not implemented yet.");
        });
    });
});


document.addEventListener("DOMContentLoaded", () => {
    // Handle "Your Pick"
    setupMovieInput({
        inputId: "your-movie-input",
        suggestionsId: "your-movie-suggestions",
        placeholderId: "your-placeholder",
    });

    // Handle "Their Pick"
    setupMovieInput({
        inputId: "their-movie-input",
        suggestionsId: "their-movie-suggestions",
        placeholderId: "their-placeholder",
    });

    function setupMovieInput({ inputId, suggestionsId, placeholderId }) {
        const movieInput = document.getElementById(inputId); // Target the input field
        const suggestionsList = document.getElementById(suggestionsId); // Target the suggestions list
        const moviePlaceholder = document.getElementById(placeholderId); // Target the correct placeholder

        // Fetch movie suggestions dynamically
        async function fetchSuggestions(query) {
            const response = await fetch(`/search_movies?query=${query}`);
            return await response.json();
        }

        // Event listener for input typing
        movieInput.addEventListener("input", async () => {
            const query = movieInput.value.trim();
            if (!query) {
                suggestionsList.classList.add("hidden"); // Hide if no input
                return;
            }

            const suggestions = await fetchSuggestions(query);
            suggestionsList.innerHTML = ""; // Clear old suggestions

            if (suggestions.length > 0) {
                suggestions.forEach((movie) => {
                    const listItem = document.createElement("li");
                    listItem.textContent = movie;

                    // On click, update the placeholder and hide the suggestions
                    listItem.addEventListener("click", () => {
                        movieInput.value = movie; // Update input field
                        moviePlaceholder.textContent = movie; // Update the placeholder
                        suggestionsList.classList.add("hidden"); // Hide suggestions
                    });

                    suggestionsList.appendChild(listItem);
                });

                suggestionsList.classList.remove("hidden"); // Show suggestions
            } else {
                suggestionsList.classList.add("hidden"); // Hide if no matches
            }
        });

        // Hide suggestions when clicking outside the input or dropdown
        document.addEventListener("click", (e) => {
            if (!movieInput.contains(e.target) && !suggestionsList.contains(e.target)) {
                suggestionsList.classList.add("hidden");
            }
        });
    }
});


document.addEventListener("DOMContentLoaded", () => {
    const diceButtons = document.querySelectorAll(".dice-button");

    diceButtons.forEach((button, index) => {
        button.addEventListener("click", async () => {
            try {
                const response = await fetch('/random_movie');
                const data = await response.json();
                const randomMovie = data.movie;

                // Find the associated placeholder
                const moviePlaceholder = button
                    .closest('.pick-card')
                    .querySelector('.movie-placeholder p');

                // Update the placeholder with the random movie
                moviePlaceholder.textContent = randomMovie;
                const inputField = button.closest(".card-controls").querySelector("input");
                inputField.value = "";
            } catch (error) {
                console.error('Error fetching random movie:', error);
                alert('Could not fetch a random movie. Please try again.');
            }
        });
    });
});

// event listener for shuffle button - get logic's recommendations 
document.addEventListener("DOMContentLoaded", () => {
    const shuffleButton = document.querySelector(".shuffle-button");
    const resultsContainer = document.getElementById("results");

    shuffleButton.addEventListener("click", async () => {
        const movie1 = document.getElementById("your-placeholder").textContent;
        const movie2 = document.getElementById("their-placeholder").textContent;

        if (movie1 === "Your Pick" || movie2 === "Their Pick") {
            alert("Please select both movies first!");
            return;
        }

        try {
            const response = await fetch("/get_movie_results", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ movie1, movie2 }),
            });

            const results = await response.json();
            console.log("this is the response I got ", results);

            if (results.error) {
                alert(results.error);
                return;
            }

            // Populate the results
            resultsContainer.innerHTML = ""; // Clear previous results
            results.forEach((movie) => {
                const resultCard = document.createElement("div");
                resultCard.classList.add("result-card");
				//ADDED
                resultCard.innerHTML = `
				    <img src="${movie.poster_url}" alt="${movie.title}" class="movie-poster">
                    <p>${movie.title}</p>
                `;
                resultsContainer.appendChild(resultCard);
            });

            // Show the results container
            resultsContainer.classList.remove("hidden");
        } catch (error) {
            console.error("Error fetching movie results:", error);
            alert("An error occurred while fetching movie results.");
        }
    });
});






