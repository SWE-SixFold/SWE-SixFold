import os
import random
import firebase_admin
from firebase_admin import firestore, credentials, auth  # Import auth for Firebase Authentication
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import omdb

# Set Project ID
os.environ["GOOGLE_CLOUD_PROJECT"] = "swe-sixfold"

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret')  # Use environment variable for secret key

# Initialize Firebase Admin SDK
firebase_admin.initialize_app()
db = firestore.client()

# OMDb API setup
omdb.set_default('apikey', os.getenv('OMDB_API_KEY', '96ae5860'))  # Use environment variable for API key

# Home / login page
@app.route('/')
def home():
    return render_template('login.html')

# Login route (for email existence check only; password check should be on the client side)
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('username')
    password = request.form.get('psw')  # Password would be verified on the client side

    try:
        # Check if the email exists in Firebase Authentication
        user = auth.get_user_by_email(email)
        flash('Login successful!')
        return render_template('index.html')
    except firebase_admin.auth.UserNotFoundError:
        flash('Invalid email or password. Please try again.')
        return redirect(url_for('home'))

# Registration route
@app.route('/register', methods=['POST', 'GET'])
def register_user():
    email = request.form.get('username')
    password = request.form.get('psw')

    try:
        # Create a new user in Firebase Authentication
        user = auth.create_user(
            email=email,
            password=password
        )
        flash('Registration successful! Please log in.')
        return redirect(url_for('home'))
    except firebase_admin.auth.EmailAlreadyExistsError:
        flash('Username (email) already exists. Please choose another.')
        return redirect(url_for('register'))

# Registration page
@app.route('/register')
def register():
    return render_template('register.html')

# Random movie route
@app.route('/random-movie')
def random_movie():
    idnum = random.randint(1000000, 9999999)
    random_id = f"tt{idnum}"
    try:
        movie = omdb.imdbid(random_id, timeout=3)
        if movie:
            return jsonify(movie)
    except Exception as e:
        return jsonify({'error': f'Movie not found or error: {str(e)}'})

    # Error if no movie found
    return jsonify({'error': 'Movie not found, try again!'})

if __name__ == "__main__":
    # Cloud Run automatically sets the PORT environment variable
    port = int(os.getenv('PORT', 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
