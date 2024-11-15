document.getElementById('profilePictureInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('profilePicturePreview').src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
});

document.getElementById('saveProfilePictureBtn').addEventListener('click', function() {
    const file = document.getElementById('profilePictureInput').files[0];
    if (file) {
        // Code to save the picture
        console.log('Save picture:', file);
    }
});

document.getElementById('saveBioBtn').addEventListener('click', function() {
    const bio = document.getElementById('bioInput').value;
    // Code to save the bio
    console.log('Save bio:', bio);
});

document.getElementById('saveProfilePictureBtn').addEventListener('click', function() {
    const button = this;
    button.textContent = 'Saved!';
    button.classList.add('btn-success');
    setTimeout(() => {
        button.textContent = 'Save Profile Picture';
        button.classList.remove('btn-success');
    }, 2000);
});

document.getElementById('saveBioBtn').addEventListener('click', function() {
    const button = this;
    button.textContent = 'Saved!';
    button.classList.add('btn-success');
    setTimeout(() => {
        button.textContent = 'Save Bio';
        button.classList.remove('btn-success');
    }, 2000);
});
