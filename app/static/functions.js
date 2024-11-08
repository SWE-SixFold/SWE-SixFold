require('dotenv').config(); // Loads environment variables from .env

const firebaseConfig = {
    apiKey: process.env.FIREBASE_API_KEY,
    authDomain: process.env.FIREBASE_AUTH_DOMAIN,
    projectId: process.env.FIREBASE_PROJECT_ID,
    storageBucket: process.env.FIREBASE_STORAGE_BUCKET,
    messagingSenderId: process.env.FIREBASE_MESSAGING_SENDER_ID,
    appId: process.env.FIREBASE_APP_ID,
};


// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// Select elements for Firebase authentication
var email = document.getElementById("email");
var password = document.getElementById("password");
var signInButton = document.getElementById("signInButton");
var signUpButton = document.getElementById("signUpButton");

// Firebase authentication: Sign in
signInButton.addEventListener("click", function() {
  firebase.auth().signInWithEmailAndPassword(email.value, password.value)
    .then(function(userCredential) {
      alert("Login successful!");
      window.location.href = "/protected-resources.html"; // Redirect to protected page
    })
    .catch(function(error) {
      alert("Login failed: " + error.message);
    });
});

// Firebase authentication: Sign up
signUpButton.addEventListener("click", function() {
    const emailValue = email.value.trim();  // Trim the email value
    const passwordValue = password.value.trim();  // Trim the password value
    
    // Validate email format
    if (!emailValue || !passwordValue) {
        alert("Email and password cannot be empty.");
        return;
    }

    // Sign up the user using Firebase's createUserWithEmailAndPassword method
    firebase.auth().createUserWithEmailAndPassword(emailValue, passwordValue)
        .then(function(userCredential) {
            alert("Registration successful!");
            window.location.href = "/protected-resources.html"; // Redirect to protected page
        })
        .catch(function(error) {
            alert("Registration failed: " + error.message);
        });
});

// Movie functionality
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
