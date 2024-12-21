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

    function setupMovieInput({ inputId, suggestionsId, placeholderId }) {
        const movieInput = document.getElementById(inputId);
        const suggestionsList = document.getElementById(suggestionsId);
        const moviePlaceholder = document.getElementById(placeholderId);

        async function fetchSuggestions(query) {
            const response = await fetch(`/search_movies?query=${query}`);
            return await response.json();
        }

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

                    listItem.addEventListener("click", async () => {
                        try {
                            movieInput.value = movie;
                            moviePlaceholder.textContent = movie;
                            suggestionsList.classList.add("hidden");
                    
                            // Fetch the movie poster URL
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

    //ADDED:
    //fixing titles. need to check if there are other cases as well
    function formatMovieTitle(title) {
        // Check if the title ends with a year in parentheses
        const yearMatch = title.match(/\s*\((\d{4})\)$/);
        const year = yearMatch ? yearMatch[0] : '';
        
        // Remove the year if it exists
        let nameOnly = yearMatch ? title.slice(0, -yearMatch[0].length) : title;
        
        // Check for any article (The, A, An) at the end of the title
        const articleMatch = nameOnly.match(/, (The|A|An)$/);
        if (articleMatch) {
            // Remove the article from the end and add it to the beginning
            nameOnly = articleMatch[1] + ' ' + nameOnly.slice(0, -(articleMatch[0].length));
        }
        
        // Return the formatted title with the year
        return `${nameOnly.trim()}${year}`;
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
                placeholder.textContent = data.movie;
                
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

                // Hide summary when using dice
                //summaryContainer.classList.remove('visible');
            } catch (error) {
                console.error('Error fetching random movie:', error);
                alert('Could not fetch a random movie. Please try again.');
            }
        });
    });

    // Set up carousel and movie summary functionality
    const carouselContainer = document.querySelector(".carousel-container");
    const summaryContainer = document.getElementById("movie-summary");
    const carouselContent = document.querySelector(".carousel-content");
    const scrollLeftButton = document.getElementById("scroll-left");
    const scrollRightButton = document.getElementById("scroll-right");

    // Add scroll button functionality
    if (scrollLeftButton && scrollRightButton) {
        scrollLeftButton.addEventListener("click", () => {
            carouselContainer.scrollBy({
                left: -200,
                behavior: "smooth"
            });
        });

        scrollRightButton.addEventListener("click", () => {
            carouselContainer.scrollBy({
                left: 200,
                behavior: "smooth"
            });
        });
    }

    async function fetchResults() {
        try {
            //the selected movies by the users
            const movie1 = document.getElementById("your-placeholder").textContent;
            const movie2 = document.getElementById("their-placeholder").textContent;
    
            if (movie1 === "Your Pick" || movie2 === "Their Pick") {
                alert("Please select both movies first!");
                return;
            }
            
           
            //fetching the returned 5 recommended movies with posters and summaries
            const response = await fetch("/get_movie_results", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ movie1, movie2 }),
            });
    
            const results = await response.json();
    
             // Clear existing content and returning to default state
             carouselContent.innerHTML = "";
             carouselContainer.scrollLeft = 0;
             //hiding summary while loading new recommendations
             summaryContainer.classList.remove('visible');
    
             showResultsContainer();

            // Show scroll buttons if there are movies
            if (results.length > 0) {
                //if (scrollLeftButton) scrollLeftButton.style.display = 'block';
                //if (scrollRightButton) scrollRightButton.style.display = 'block';
                
                // Create and append movie cards
                results.forEach((movie) => {
                    const card = document.createElement("div");
                    card.classList.add("result-card");
                    

                    if (movie.poster_url && !movie.poster_url.includes("placeholder")) {
                        card.innerHTML = `<img src="${movie.poster_url}" alt="${movie.title}">`;
                    } else {
                        card.innerHTML = `<div class="movie-title">${movie.title}</div>`;
                    }

                    //card.innerHTML = `
                    //    <img src="${movie.poster_url}" alt="${movie.title}">
                    //`;
    
                    card.addEventListener("click", () => {
                        const formattedTitle = formatMovieTitle(movie.title);
                        summaryContainer.classList.add('visible');
                        summaryContainer.innerHTML = `
                            <h2>${formattedTitle}</h2>
                            <p>${movie.summary || "No summary available."}</p>
                        `;
                        
                        document.querySelectorAll('.result-card').forEach(c => 
                            c.style.transform = 'scale(1)');
                        card.style.transform = 'scale(1.05)';
                    });
    
                    carouselContent.appendChild(card);
                });
    
                // Show the summary for the first movie after a short delay
                setTimeout(() => {
                    const formattedTitle = formatMovieTitle(results[0].title);
                    summaryContainer.classList.add('visible');
                    summaryContainer.innerHTML = `
                        <h2>${formattedTitle}</h2>
                        <p>${results[0].summary || "No summary available."}</p>
                    `;
                }, 100);
            }
    
        } catch (error) {
            console.error("Error fetching movie results:", error);
            summaryContainer.innerHTML = "<p>Error loading movie information.</p>";
        }
    }

    // Hide summary when typing in movie inputs
   // const movieInputs = document.querySelectorAll("#your-movie-input, #their-movie-input");
   // movieInputs.forEach(input => {
   //     input.addEventListener("input", () => {
   //         summaryContainer.classList.remove('visible');
   //     });
   // });
    
   function showResultsContainer() {
    const resultsContainer = document.querySelector('.results-container');
    if (resultsContainer) {
        resultsContainer.style.display = 'flex';
    }
    if (scrollLeftButton) scrollLeftButton.style.display = 'block';
    if (scrollRightButton) scrollRightButton.style.display = 'block';
}

function hideResultsContainer() {
    const resultsContainer = document.querySelector('.results-container');
    if (resultsContainer) {
        resultsContainer.style.display = 'none';
    }
    if (scrollLeftButton) scrollLeftButton.style.display = 'none';
    if (scrollRightButton) scrollRightButton.style.display = 'none';
}

// Attach click handler to shuffle button
const shuffleButton = document.querySelector(".shuffle-button");
if (shuffleButton) {
    shuffleButton.addEventListener("click", fetchResults);
} else {
    console.error("Error: Shuffle button not found!");
}
});