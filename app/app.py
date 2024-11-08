import os
import random
<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pyrebase
import requests
from firebase_admin import credentials, initialize_app, auth, firestore
import firebase_admin
from functools import wraps
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Firebase Admin
cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS_PATH'))  # Load path from .env
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Firebase Authentication
firebase_config = {
    'apiKey': os.getenv('FIREBASE_API_KEY'),
    'authDomain': os.getenv('FIREBASE_AUTH_DOMAIN'),
    'databaseURL': os.getenv('FIREBASE_DATABASE_URL'),
    'projectId': os.getenv('FIREBASE_PROJECT_ID'),
    'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET'),
    'messagingSenderId': os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
    'appId': os.getenv('FIREBASE_APP_ID'),
    'measurementId': os.getenv('FIREBASE_MEASUREMENT_ID'),
}
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# OMDB API key (stored in .env for security)
OMDB_API_KEY = os.getenv('OMDB_API_KEY')

# Decorator to require login for certain routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Root route to redirect to home
@app.route('/')
def root():
    return redirect(url_for('home'))

# Home page route
@app.route('/home')
def home():
    return render_template('index.html')

# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['psw']
        try:
            user = auth.create_user_with_email_and_password(username, password)
            return redirect(url_for('login'))
        except Exception as e:
            return f'Error: {str(e)}'
    return render_template('register.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['psw']
        try:
            user = auth.sign_in_with_email_and_password(username, password)
            session['user'] = user['localId']
            return redirect(url_for('home'))  # Ensure it redirects to home or index
        except Exception as e:
            return f'Error: {str(e)}'
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove user from session
    return redirect(url_for('home'))

# Search movie route
@app.route('/search-movie')
def search_movie():
    movie_title = request.args.get('query')
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    
    response = requests.get(url)
    data = response.json()
    
    if data['Response'] == 'True':
        return jsonify({
            'title': data['Title'],
            'year': data['Year'],
            'plot': data['Plot'],
            'poster': data['Poster']
        })
    else:
        return jsonify({'error': data['Error']})

# Random movie route
@app.route('/random')
def random_movie():
    for _ in range(5):  # Retry up to 5 times if the movie is invalid
        random_id = f"tt{random.randint(1000000, 9999999)}"  # Generate a random IMDB ID
        url = f"http://www.omdbapi.com/?i={random_id}&apikey={OMDB_API_KEY}"
        
        response = requests.get(url)
        data = response.json()
        
        if data['Response'] == 'True':  # Valid response from OMDB
            return jsonify({
                'title': data['Title'],
                'year': data['Year'],
                'plot': data['Plot'],
                'poster_path': data['Poster']
            })
    
    return jsonify({'error': 'Could not retrieve a valid random movie after multiple attempts'})

# Error page (if no route matches)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
=======
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
>>>>>>> 120632e8c2a424c011bc2e69debccf4495e627ab
