import os
import random
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import omdb

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'sssecret'  # Replace with a strong secret key

# Initialize Firestore
cred = credentials.Certificate(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
firebase_admin.initialize_app(cred)
db = firestore.client()

# OMDb API setup
omdb.set_default('apikey', '96ae5860')

# Home / login page
@app.route('/')
def home():
    return render_template('login.html')

# Login route
@app.route('/login', methods=['POST', 'GET'])
def login():
    username = request.form.get('username')
    password = request.form.get('psw')

    # Retrieve user with matching username and password
    user_ref = db.collection('users').where('username', '==', username).where('password', '==', password).stream()
    user = next(user_ref, None)  # Get first matching user or None if no match

    if user:
        flash('Login successful!')
        return render_template('index.html')
    else:
        flash('Invalid username or password. Please try again.')
        return redirect(url_for('home'))

# Registration route
@app.route('/register', methods=['POST', 'GET'])
def register_user():
    username = request.form.get('username')
    password = request.form.get('psw')

    # Check if username already exists
    user_ref = db.collection('users').where('username', '==', username).stream()
    if any(user_ref):  # If any user exists with that username
        flash('Username already exists. Please choose another.')
        return redirect(url_for('register'))
    
    # Add new user to Firestore
    db.collection('users').add({
        'username': username,
        'password': password
    })
    flash('Registration successful! Please log in.')
    return redirect(url_for('home'))

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
    except:
        pass

    # Error if no movie found
    return jsonify({'error': 'Movie not found, try again!'})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
