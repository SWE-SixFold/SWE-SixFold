// Toggles the visibility of the dropdown menu (show/hide)
function toggleMenu() {
    const menu = document.getElementById('dropdownMenu');
    if (menu) {
        menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
    }
}

// Listens for clicks anywhere on the document to close dropdown when clicking outside
document.addEventListener('click', function(event) {
    const menu = document.getElementById('dropdownMenu');
    const profileIcon = document.querySelector('.profile-icon');

    if (menu && !profileIcon.contains(event.target)) {
        menu.style.display = 'none';
    }
});

// Toggles dark mode on and off by adding/removing the "dark-mode" class
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
}

// Function to handle "random" button click
function feelingLucky() {
    fetch('/random-movie')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(`Title: ${data.title}\nYear: ${data.year}\nPlot: ${data.plot}`);
            }
        })
        .catch(error => {
            console.error('Error fetching movie:', error);
            alert('Failed to fetch a random movie, please try again.');
        });
}

// API Key for OMDB (replace with your own key)
const apiKey = '96ae5860'; // Replace with your OMDB API key

// Function to search for a movie by title
function searchMovie() {
    const movieTitle = document.getElementById('movieInput').value;
    const url = `https://www.omdbapi.com/?t=${encodeURIComponent(movieTitle)}&apikey=${apiKey}`;

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const resultDiv = document.getElementById('result');
            if (data.Response === 'True') {
                resultDiv.innerHTML = `
                    <h2>${data.Title} (${data.Year})</h2>
                    <img src="${data.Poster}" alt="${data.Title}">
                    <p>${data.Plot}</p>
                `;
            } else {
                resultDiv.innerHTML = `<p>${data.Error}</p>`;
            }
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

// Function to show the login modal with frosted background effect and smooth blur transition
function showLoginModal() {
    const frostedBackground = document.getElementById('frostedBackground');
    const loginModal = document.getElementById('loginModal');

    frostedBackground.style.display = 'block';
    loginModal.style.display = 'block';

    frostedBackground.style.transition = 'backdrop-filter 0.3s ease';
    frostedBackground.style.backdropFilter = 'blur(8px)';
}

// Function to hide the login modal
function hideLoginModal() {
    const frostedBackground = document.getElementById('frostedBackground');
    const loginModal = document.getElementById('loginModal');

    frostedBackground.style.display = 'none';
    frostedBackground.style.backdropFilter = 'blur(0px)';
    loginModal.style.display = 'none';
}

// Event listener for hiding modal and frosted background when clicking outside
document.addEventListener('click', function(event) {
    const frostedBackground = document.getElementById('frostedBackground');
    const loginModal = document.getElementById('loginModal');
    const profileIcon = document.querySelector('.profile-icon');

    if (frostedBackground.style.display === 'block' && !loginModal.contains(event.target) && !profileIcon.contains(event.target)) {
        hideLoginModal();
    }
});

// Add event listener for messages from the iframe
window.addEventListener('message', function(event) {
    var iframeHeight = event.data;

    // Set the iframe height
    var iframe = document.querySelector('.login-iframe');
    iframe.style.height = iframeHeight + 'px';
}, false);

// Hide the modal when clicking on the frosted background
document.getElementById('frostedBackground').addEventListener('click', hideLoginModal);

function enableEditing() {
    const editableFields = document.querySelectorAll('.editable');
    editableFields.forEach(field => field.contentEditable = 'true');

    // Change Edit button to Save button
    const editButton = document.querySelector('.edit-button');
    editButton.textContent = "Save Profile";
    editButton.onclick = saveProfile;
}

function saveProfile() {
    const editableFields = document.querySelectorAll('.editable');
    const profileData = {};

    editableFields.forEach(field => {
        field.contentEditable = 'false';
        profileData[field.id] = field.textContent;
    });

    // Placeholder for sending updated profile data to backend
    console.log("Saved Profile Data:", profileData);

    const saveButton = document.querySelector('.edit-button');
    saveButton.textContent = "Save Profile";
    saveButton.onclick = enableEditing;
}

function loadFavoriteMovies() {
    // Placeholder: Fetch favorite movies from the backend and render
    const moviesGallery = document.getElementById('moviesGallery');
    const movies = ["Movie 1", "Movie 2", "Movie 3"];  // Replace with backend data *****

    movies.forEach(movie => {
        const movieCard = document.createElement('div');
        movieCard.classList.add('movie-card');
        movieCard.textContent = movie;
        moviesGallery.appendChild(movieCard);
    });
}

// Define the idle timeout duration (in milliseconds)
const idleTimeout = 20 * 60 * 1000; // 20 minutes

let idleTimer;

// Function to reset the idle timer
function resetIdleTimer() {
    clearTimeout(idleTimer);
    idleTimer = setTimeout(logoutUser, idleTimeout);
}

// Function to log out the user
function logoutUser() {
    alert("You have been logged out due to inactivity.");
    window.location.href = "/logout"; // Redirect to logout route or URL
}

// Event listeners for user activity
window.onload = resetIdleTimer;
window.onmousemove = resetIdleTimer;
window.onkeypress = resetIdleTimer;
window.onscroll = resetIdleTimer;
window.onclick = resetIdleTimer;

// Run on page load
document.addEventListener("DOMContentLoaded", loadFavoriteMovies);

/* Function to save darkmode pref to all pages
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');

    // Save the user's dark mode preference
    if (document.body.classList.contains('dark-mode')) {
        localStorage.setItem('darkMode', 'enabled');
    } else {
        localStorage.setItem('darkMode', 'disabled');
    }
}

// Check and apply the dark mode preference on page load
document.addEventListener('DOMContentLoaded', () => {
    const darkModePreference = localStorage.getItem('darkMode');
    if (darkModePreference === 'enabled') {
        document.body.classList.add('dark-mode');
    }
}); */