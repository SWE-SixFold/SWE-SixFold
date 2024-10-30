// toggles the visibility of the dropdown menu (show/hide)
function toggleMenu() {
    const menu = document.getElementById('dropdownMenu'); // get the dropdown menu by its ID
    if (menu) { // if the menu exists on the page
        // toggle display: if it's "block" (visible), set to "none"; if "none" (hidden), set to "block"
        menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
    }
}



// listens for clicks anywhere on the document to close dropdown when clicking outside
document.addEventListener('click', function(event) {
    const menu = document.getElementById('dropdownMenu'); // get the dropdown menu
    const profileIcon = document.querySelector('.profile-icon'); // get the profile icon area

    // if the click was outside the profile icon area, hide the menu
    if (menu && !profileIcon.contains(event.target)) {
        menu.style.display = 'none';
    }
});

// toggles dark mode on and off by adding/removing the "dark-mode" class
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode'); // if dark mode is active, turn it off, and vice versa
}


// function to handle "random" button click
function feelingLucky() {
    //  call flask for a random movie
    fetch('/random-movie')
        .then(response => response.json()) // json response from flask
        .then(data => {
            if (data.error) {
                alert(data.error); // show error message if no movie was found
            } else {
                // show the movie details in an alert (alert for testing, will in the future show a full webpage possibly)
                alert(`Title: ${data.title}\nYear: ${data.year}\nPlot: ${data.plot}`);
            }
        })
        .catch(error => {
            console.error('Error fetching movie:', error);
            alert('Failed to fetch a random movie, please try again.');
        });
}

const apiKey = '96ae5860'; // Replace with your OMDB API key

function searchMovie() {
    const movieTitle = document.getElementById('movieInput').value; // Get movie title from input field
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

// Handle Login and Registration inputs to create accounts. Entering username "user" and password "web_dev" logs you in.

/*

const loginButton = document.getElementById("login-form-submit");

loginButton.addEventListener("click", (e) => {
    e.preventDefault();

    const loginForm = document.getElementById("login-form");
    const username = loginForm.username.value;
    const password = loginForm.psw.value;

    if (username === "user" && password === "web_dev") {
        alert("You have successfully logged in.");
        window.location.href = "index.html";
    } else {
        alert("Login failed. Please try again.");
    }
}) */