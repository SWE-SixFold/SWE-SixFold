// Function to expand the details box with the selected poster
function expandDetails(event, posterUrl, title, ratings, plot, imdbUrl) {
    console.log("Poster clicked:", title, ratings, plot, imdbUrl); // Log data for debugging

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