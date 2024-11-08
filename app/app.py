import os
import random
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import pyrebase
import requests
from firebase_admin import credentials, initialize_app, auth, firestore
import firebase_admin
import re
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

# Firebase Authentication Configuration
firebase_config = {
    'apiKey': os.getenv('FIREBASE_API_KEY'),
    'authDomain': os.getenv('FIREBASE_AUTH_DOMAIN'),
    'databaseURL': os.getenv('FIREBASE_DATABASE_URL'),
    'projectId': os.getenv('FIREBASE_PROJECT_ID'),
    'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET'),
    'messagingSenderId': os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
    'appId': os.getenv('FIREBASE_APP_ID'),
}
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# OMDB API key (stored in .env for security)
OMDB_API_KEY = os.getenv('OMDB_API_KEY')

# Decorator to require login for certain routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id_token' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Root route to redirect to home
@app.route('/')
def index():
    if 'id_token' not in session:
        return redirect(url_for('login'))  # If not logged in, redirect to login page
    return render_template('index.html')  # Serve the index.html page

# Home route
@app.route('/home')
@login_required  # Protect home route with login_required decorator
def home():
    try:
        # Get user info using the ID token
        user_info = auth.get_account_info(session['id_token'])
        return render_template('home.html', user=user_info)
    except:
        return redirect(url_for('login'))  # If token is invalid or expired, redirect to login page

# Email validation
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        email = request.form['email'].strip()
        password = request.form['psw']
        confirm_password = request.form['psw-repeat']

        # Check if email is valid
        if not is_valid_email(email):
            flash("Invalid email format", "error")
            return redirect(url_for('register'))

        # Check if the passwords match
        if password != confirm_password:
            flash("Passwords do not match", "error")
            return redirect(url_for('register'))

        try:
            # Create user in Firebase
            user = auth.create_user_with_email_and_password(email, password)
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))  # Redirect to login page after successful registration
        except Exception as e:
            flash(f"Error: {str(e)}", "error")
            return redirect(url_for('register'))
    
    return render_template('register.html')  # Render the registration form

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['psw']

        try:
            # Log in the user with Firebase Authentication
            user = auth.sign_in_with_email_and_password(email, password)
            
            # Store the user's ID token in the session
            session['id_token'] = user['idToken']
            flash("Login successful!", "success")

            # Redirect to homepage after successful login
            return redirect(url_for('index'))  # Redirect to 'index' page

        except Exception as e:
            flash(f"Login failed: {str(e)}", "error")
            return redirect(url_for('login'))

    return render_template('login.html')  # Render the login form

# Logout route
@app.route('/logout')
def logout():
    session.pop('id_token', None)  # Remove the id_token from session to log out
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
