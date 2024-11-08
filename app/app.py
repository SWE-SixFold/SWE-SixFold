import os
import random
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import pyrebase
import requests
from firebase_admin import credentials, auth, firestore
import firebase_admin
import re
from functools import wraps
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

@app.route('/profile')
@login_required
def profile():
    # Get the user information from the session
    user_info = auth.get_account_info(session['id_token'])
    user_email = user_info['users'][0]['email']

    # Fetch favorite movies from the database (Firestore or another storage)
    user_ref = db.collection('users').document(user_email)
    favorites_ref = user_ref.collection('favorites')
    favorite_movies = favorites_ref.stream()

    # Prepare the list of favorite movies
    movies = []
    for movie in favorite_movies:
        movie_data = movie.to_dict()
        movie_data['id'] = movie.id
        movies.append(movie_data)

    return render_template('profile.html', user=user_info['users'][0], favorite_movies=movies)

@app.route('/add-favorite', methods=['POST'])
@login_required
def add_favorite():
    movie = request.get_json()
    movie_id = movie['movieId']
    title = movie['title']
    year = movie['year']
    poster = movie['poster']

    # Get the current user from the session
    user_info = auth.get_account_info(session['id_token'])
    user_email = user_info['users'][0]['email']

    # Add the movie to the user's favorite movies collection
    user_ref = db.collection('users').document(user_email)
    favorites_ref = user_ref.collection('favorites')
    
    # Check if the movie is already in favorites
    existing_movie = favorites_ref.where('movieId', '==', movie_id).get()
    if existing_movie:
        return jsonify({'success': False, 'message': 'Movie already in favorites'})

    # Add new movie to the favorites
    favorites_ref.add({
        'movieId': movie_id,
        'title': title,
        'year': year,
        'poster': poster
    })

    return jsonify({'success': True})

@app.route('/remove-favorite/<movie_id>', methods=['DELETE'])
@login_required
def remove_favorite(movie_id):
    # Get the current user from the session
    user_info = auth.get_account_info(session['id_token'])
    user_email = user_info['users'][0]['email']

    # Delete the movie from the user's favorites collection
    user_ref = db.collection('users').document(user_email)
    favorites_ref = user_ref.collection('favorites')
    
    movie_ref = favorites_ref.document(movie_id)
    movie_ref.delete()

    return jsonify({'success': True})

# Route for the settings page
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    # Assuming the user is authenticated and their UID is stored in the session
    user_uid = session.get('user_uid')  # Replace with actual method of getting user UID from session

    if not user_uid:
        return redirect(url_for('login'))  # Redirect to login if no UID is found

    # Fetch user data from Firestore
    user_ref = db.collection('users').document(user_uid)
    user_doc = user_ref.get()

    if not user_doc.exists:
        return 'User not found', 404

    user_data = user_doc.to_dict()

    current_username = user_data.get('username', '')
    current_email = user_data.get('email', '')

    if request.method == 'POST':
        # Handle form submission to update user data
        new_username = request.form['username']
        new_email = request.form['email']
        
        # Update the user data in Firestore
        user_ref.update({
            'username': new_username,
            'email': new_email
        })

        return redirect(url_for('settings'))  # Redirect back to the settings page after updating

    return render_template('settings.html', current_username=current_username, current_email=current_email)

 # Route for forgot_password
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        try:
            link = auth.generate_password_reset_link(email)
            print(f"Password reset link: {link}")
            flash("Password reset link sent! Check your email.", "success")
            return redirect(url_for('login'))
        except auth.AuthError as e:
            flash("Error sending password reset email: " + str(e), "error")
    return render_template('forgot_password.html')


def send_reset_email(email, reset_link):
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "swe.cinesage@gmail.com"
        sender_password = "sagepass"

        # Set up the MIME
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = email
        message['Subject'] = "Password Reset"

        # Email body
        body = f"Click the following link to reset your password: {reset_link}"
        message.attach(MIMEText(body, 'plain'))

        # Start SMTP session
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable security
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message.as_string())
        server.quit()
        
        print("Password reset email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)

# Error page (if no route matches)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
