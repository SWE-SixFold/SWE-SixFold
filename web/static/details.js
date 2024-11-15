// Function to expand the details box with the selected poster
function expandDetails(event, posterUrl, title, ratings, plot, imdbUrl) {
    console.log("Poster clicked:", title, ratings, plot, imdbUrl); // Log data for debugging

    const detailsBox = document.getElementById("details-box");
    const expandedPoster = document.getElementById("expanded-poster");
    const movieRating = document.getElementById("movie-rating");
    const movieSynopsis = document.getElementById("movie-synopsis");
    const imdbLink = document.getElementById("imdb-link");
    const synopsisImdbLink = document.getElementById("synopsis-imdb-link");

    // Set the poster, ratings, and synopsis
    expandedPoster.src = posterUrl;
    movieRating.textContent = ratings && ratings !== "N/A" ? ratings : "Rating unavailable";
    movieSynopsis.textContent = plot && plot !== "N/A" ? plot : "No synopsis available";

    // Handle IMDb links
    imdbLink.href = imdbUrl ? imdbUrl : "https://www.imdb.com/";
    synopsisImdbLink.href = imdbUrl ? imdbUrl : "https://www.imdb.com/";
    synopsisImdbLink.classList.toggle("hidden", !plot || plot === "N/A");

    // Positioning the details box near the clicked poster
    const posterRect = event.currentTarget.getBoundingClientRect();
    const boxWidth = detailsBox.offsetWidth;
    const boxHeight = detailsBox.offsetHeight;
    const viewportMidpoint = window.innerWidth / 2;

    let top = posterRect.top + window.scrollY;
    let left;

    // Check if the poster is on the left or right of the viewport midpoint
    if (posterRect.left < viewportMidpoint) {
        // Position to the right of the poster
        left = posterRect.right + 10;
        // Adjust if it overflows the right side
        if (left + boxWidth > window.innerWidth) {
            left = window.innerWidth - boxWidth - 500;
        }
    } else {
        // Position to the left of the poster
        left = posterRect.left - boxWidth - 410;
        // Adjust if it overflows the left side
        if (left < 0) {
            left = 20;
        }
    }

    // Check if the box goes off-screen at the bottom and adjust if needed
    if (top + boxHeight > window.innerHeight + window.scrollY) {
        top = window.innerHeight + window.scrollY - boxHeight - 20;
    }

    // Ensure the box stays within viewport at the top
    if (top < window.scrollY) {
        top = window.scrollY + 20;
    }

    // Apply calculated positions
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
    detailsBox.classList.remove("visible");

    // Remove the outside click event listener when closed
    document.removeEventListener('click', handleClickOutside);
}

// Function to handle clicks outside of the details box
function handleClickOutside(event) {
    const detailsBox = document.getElementById("details-box");
    if (!detailsBox.contains(event.target) && !event.target.classList.contains("image-item")) {
        closeDetails();
    }
}

// Function to add the movie to the watchlist
function addToWatchlist() {
    alert("Movie added to watchlist!");
}

// Function to add the movie to favorites
function addToFavorites() {
    alert("Movie added to favorites!");
}

// Function to toggle the note box visibility
function toggleNoteBox() {
    const noteBox = document.getElementById("note-box");
    noteBox.classList.toggle("visible");
}

// Function to save a note
function saveNote() {
    const noteInput = document.getElementById("note-input");
    if (noteInput.value.trim() !== "") {
        alert(`Note saved: ${noteInput.value}`);
        noteInput.value = "";
        toggleNoteBox();
    } else {
        alert("Please enter a note before saving.");
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