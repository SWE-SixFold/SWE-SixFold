// Function to expand the details box with the selected poster
function expandDetails(event, posterUrl, title, ratings, plot, imdbUrl, imdb_id) {
    console.log("Poster clicked:", title, ratings, plot, imdbUrl); // Log data for debugging
    
    document.getElementById('current-movie-title').value = title; // Store the title
    console.log(`Movie selected: ${title}`); // Debugging log

    const detailsBox = document.getElementById("details-box");
    const noteInput = document.getElementById("note-input");
    

    // Close the details box if it is already visible
    if (detailsBox.classList.contains("visible")) {
        if (noteInput.value.trim() === "") {
            closeDetails();
        } else {
            alert("Finish typing your note before switching!");
            return;
        }
    }

    // Populate the details box content
    const expandedPoster = document.getElementById("expanded-poster");
    const movieRating = document.getElementById("movie-rating");
    const movieSynopsis = document.getElementById("movie-synopsis");
    const imdbLink = document.getElementById("imdb-link");
    const synopsisImdbLink = document.getElementById("synopsis-imdb-link");

    expandedPoster.src = posterUrl;
    movieRating.textContent = ratings && ratings !== "N/A" ? ratings : "Rating unavailable";
    movieSynopsis.textContent = plot && plot !== "N/A" ? plot : "No synopsis available";

    imdbLink.href = imdbUrl ? imdbUrl : "https://www.imdb.com/";
    synopsisImdbLink.href = imdbUrl ? imdbUrl : "https://www.imdb.com/";
    synopsisImdbLink.classList.toggle("hidden", !plot || plot === "N/A");

    // ** Add Title to Details Box ** //
    // Create or update the title element in the details box
    const titleElement = document.createElement("h2"); // Create a new <h2> for the title
    titleElement.textContent = title; // Set the title text

    // Clear any existing title (if present)
    const existingTitle = detailsBox.querySelector("h2"); // Look for an existing <h2> in the box
    if (existingTitle) {
        existingTitle.remove(); // Remove the old title if found
    }
    detailsBox.prepend(titleElement); // Add the new title to the top of the details box

    // ** Fetch Request to send the movie title to Flask ** //
    fetch('/save-movie-title', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            title: title,   // Sending the movie title
            poster: posterUrl,
            ratings: ratings,
            plot: plot,
            imdbUrl: imdbUrl
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Title saved:", data.message); // Log a success message from Flask
    })
    .catch(error => {
        console.error("Error:", error); // Log any error that occurs
    });
    
    // ** Button Event Listeners ** //
    const saveToWatchlistBtn = document.getElementById('add-to-watchlist');
    const addToFavoritesBtn = document.getElementById('add-to-favorites');


    // Handle Save to Watchlist button click
    saveToWatchlistBtn.addEventListener('click', function() {
        fetch('/add-to-watchlist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ imdb_id: imdb_id })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // Handle Add to Favorites button click
    addToFavoritesBtn.addEventListener('click', function() {
        fetch('/add-to-favorites', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ imdb_id: imdb_id })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // Position the details box near the clicked poster
    const posterRect = event.currentTarget.getBoundingClientRect();
    const boxWidth = detailsBox.offsetWidth;
    const boxHeight = detailsBox.offsetHeight;
    const viewportMidpoint = window.innerWidth / 2;

    let top = posterRect.top + window.scrollY;
    let left;

    if (posterRect.left < viewportMidpoint) {
        left = posterRect.right + 10;
        if (left + boxWidth > window.innerWidth) {
            left = window.innerWidth - boxWidth - 500; 
        }
    } else {
        left = posterRect.left - boxWidth - 410; 
        if (left < 0) {
            left = 20;
        }
    }

    if (top + boxHeight > window.innerHeight + window.scrollY) {
        top = window.innerHeight + window.scrollY - boxHeight - 20;
    }

    if (top < window.scrollY) {
        top = window.scrollY + 20;
    }

    detailsBox.style.top = `${top}px`;
    detailsBox.style.left = `${left}px`;

    // Show the details box
    detailsBox.classList.add("visible");

    // Add event listener to close the details box when clicking outside of it
    setTimeout(() => document.addEventListener('click', handleClickOutside), 0);
}

// Function to close the expanded details box
function closeDetails() {
    const detailsBox = document.getElementById("details-box");
    const noteBox = document.getElementById("note-box");
    const noteInput = document.getElementById("note-input");

    // Reset the note box if it's empty
    if (noteInput.value.trim() === "") {
        noteBox.classList.remove("visible");
    }

    detailsBox.classList.remove("visible");

    // Remove the outside click event listener when closed
    document.removeEventListener('click', handleClickOutside);
}

// Function to handle clicks outside of the details box
function handleClickOutside(event) {
    const detailsBox = document.getElementById("details-box");
    const noteBox = document.getElementById("note-box");

    if (
        !detailsBox.contains(event.target) &&
        !event.target.classList.contains("image-item") &&
        !noteBox.contains(event.target)
    ) {
        closeDetails();
    }
}

// Function to toggle the note box visibility
function toggleNoteBox() {
    const noteBox = document.getElementById("note-box");
    noteBox.classList.toggle("visible");
}

// Function to save a note
function saveNote() {
    const noteInput = document.getElementById("note-input");
    const noteText = noteInput.value.trim();
    const movieTitle = document.getElementById("current-movie-title").value; // Get the title

    if (noteText !== "" && movieTitle !== "") {
        // Sending the note and title to Flask using Fetch API (AJAX)
        fetch('/save_note', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                note: noteText, 
                movie_title: movieTitle  // Include the movie title
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert(`Note saved for "${movieTitle}": ${noteText}`);
                noteInput.value = ""; // Clear the input
                toggleNoteBox(); // Hide the note box
            } else {
                alert("Error saving note.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Failed to save note.");
        });
    } else {
        alert("Please enter a note and ensure the movie title is available.");
    }
}


// Function to discard a note
function discardNote() {
    const noteInput = document.getElementById("note-input");
    noteInput.value = "";
    toggleNoteBox();
}

// Ensure buttons inside the details box don’t trigger the handleClickOutside event
document.getElementById("details-box").addEventListener('click', function(event) {
    event.stopPropagation();
});