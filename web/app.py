# app.py

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from firebase_admin import credentials, initialize_app, auth, firestore
import requests
import random
import os

app = Flask(__name__, static_folder ='static')
app.secret_key = os.getenv("SECRET_KEY")

# Initialize Firebase
cred = credentials.Certificate("swe-sixfold-firebase-adminsdk-ceb23-14f07f09f7.json")
firebase_app = initialize_app(cred)
db = firestore.client()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

# Route to serve the main landing page (index.html)
@app.route("/")
def index():
    image_url = url_for('static', filename='images/profile-placeholder.png')
    return render_template("index.html", image_url=image_url)

# Route for searching movies with OMDb API
@app.route("/results", methods=["GET"])
def results():
    movie_title = request.args.get("movieTitle")
    genre = request.args.get("genre")

    if not movie_title:
        return jsonify({"error": "No movie title provided"}), 400

    omdb_url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={movie_title}"
    if genre:
        omdb_url += f"&genre={genre}"

    response = requests.get(omdb_url)
    if response.status_code == 200:
        movies = response.json().get("Search", [])
        return render_template("results.html", movies=movies)
    else:
        return jsonify({"error": "Failed to fetch movies"}), 500

# Login route (connects to Firebase auth)
@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")
    try:
        user = auth.get_user_by_email(email)
        session["user"] = user.email
        return jsonify({"success": True, "user": user.email}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Logout route
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

random_keywords = ["adventure", "action", "comedy", "drama", "fantasy", "horror", "romance", "thriller"]

# Random Button using keyword
@app.route("/random-movie", methods=["GET"])
def random_movie():
    # Pick a random keyword from the list
    keyword = random.choice(random_keywords)

    # Search OMDb API using the random keyword
    omdb_url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={keyword}"
    response = requests.get(omdb_url)

    if response.status_code == 200:
        movies = response.json().get("Search", [])
        return render_template("results.html", movies=movies)
    else:
        return jsonify({"error": "Failed to fetch random movies"}), 500
    
# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

