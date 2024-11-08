// Handles the random movie button click
const randomButton = document.querySelector('.button-group button:last-child');
const movieDisplayArea = document.getElementById('movie-display'); // Container to display the movie results

randomButton.addEventListener('click', () => {
    fetchRandomMovie(); // Fetch a random movie and display it
});

// Handles the movie search button click
const searchButton = document.querySelector('.button-group button:first-child');
const searchInput = document.querySelector('.search-box input[type="text"]');

searchButton.addEventListener('click', () => {
    const query = searchInput.value.trim();
    if (query) {
        searchMovies(query); // Search movies based on the query entered
    }
});

// Check if dark mode was previously enabled
if (localStorage.getItem("darkMode") === "enabled") {
    document.body.classList.add("dark-mode");
}

function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
    // Save the preference to local storage
    if (document.body.classList.contains("dark-mode")) {
        localStorage.setItem("darkMode", "enabled");
    } else {
        localStorage.setItem("darkMode", "disabled");
    }
}

// Search Movie by Title
function searchMovie() {
    const query = document.getElementById('movieInput').value.trim(); // Get the movie input

    if (!query) {
        document.getElementById("movie-display").innerHTML = "<p>Please enter a movie title.</p>";
        return; // Exit if the input is empty
    }

    fetch(`/search-movie?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("movie-display").innerHTML = `<p>${data.error}</p>`;
            } else {
                document.getElementById("movie-display").innerHTML = `
                    <h2>${data.title}</h2>
                    <p>Year: ${data.year}</p>
                    <p>Plot: ${data.plot}</p>
                    <img src="${data.poster}" alt="Movie Poster">
                `;
            }
        })
        .catch(error => {
            console.error('Error fetching movie:', error);
            document.getElementById("movie-display").innerHTML = `<p>Failed to load movie data.</p>`;
        });
}


function fetchRandomMovie() {
    fetch('/random')
        .then(response => response.json())
        .then(data => {
            console.log('Random movie data received:', data); // Log the received data
            if (data.error) {
                document.getElementById("movie-display").innerHTML = `<p>${data.error}</p>`;
            } else {
                document.getElementById("movie-display").innerHTML = `
                    <h2>${data.title}</h2>
                    <p>Year: ${data.year}</p>
                    <img src="${data.poster_path}" alt="Movie Poster">
                    <p>Plot: ${data.plot}</p>
                `;
            }
        })
        .catch(error => {
            console.error('Error fetching random movie:', error);
            document.getElementById("movie-display").innerHTML = `<p>Failed to load movie data.</p>`;
        });
}
