// Select elements
const randomButton = document.getElementById('randomMovieButton');
const searchButton = document.getElementById('searchMovieButton');
const searchInput = document.getElementById('movieInput');
const movieDisplayArea = document.getElementById('movie-display'); // Container to display the movie results

// Add event listener for random movie button
randomButton.addEventListener('click', fetchRandomMovie);

// Add event listener for search button
searchButton.addEventListener('click', () => {
    const query = searchInput.value.trim();
    if (query) {
        searchMovie(query); // Search movies based on the query entered
    } else {
        movieDisplayArea.innerHTML = "<p>Please enter a movie title.</p>";
    }
});

// Check if dark mode was previously enabled
if (localStorage.getItem("darkMode") === "enabled") {
    document.body.classList.add("dark-mode");
}

// Dark mode toggle function
function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
    // Save the preference to local storage
    if (document.body.classList.contains("dark-mode")) {
        localStorage.setItem("darkMode", "enabled");
    } else {
        localStorage.setItem("darkMode", "disabled");
    }
}

// Search Movie by Title function
function searchMovie(query) {
    fetch(`/search-movie?query=${encodeURIComponent(query)}`)
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            if (data.error) {
                movieDisplayArea.innerHTML = `<p>${data.error}</p>`;
            } else {
                movieDisplayArea.innerHTML = `
                    <h2>${data.title}</h2>
                    <p>Year: ${data.year}</p>
                    <p>Plot: ${data.plot}</p>
                    <img src="${data.poster}" alt="Movie Poster">
                `;
            }
        })
        .catch(error => {
            console.error('Error fetching movie:', error);
            movieDisplayArea.innerHTML = `<p>Failed to load movie data.</p>`;
        });
}

// Fetch Random Movie function
function fetchRandomMovie() {
    fetch('/random')
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            console.log('Random movie data received:', data); // Log the received data
            if (data.error) {
                movieDisplayArea.innerHTML = `<p>${data.error}</p>`;
            } else {
                movieDisplayArea.innerHTML = `
                    <h2>${data.title}</h2>
                    <p>Year: ${data.year}</p>
                    <img src="${data.poster_path}" alt="Movie Poster">
                    <p>Plot: ${data.plot}</p>
                `;
            }
        })
        .catch(error => {
            console.error('Error fetching random movie:', error);
            movieDisplayArea.innerHTML = `<p>Failed to load movie data.</p>`;
        });
}
