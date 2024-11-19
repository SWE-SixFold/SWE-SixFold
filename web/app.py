import os
import pymysql
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import pymysql.cursors
import omdb

"""
TODO 
    things I need to add: what if same username, 
    how to check confirm password on html thing, 
    how to make sure page only works with people signed in and how
"""

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Connect to SQL function
def connect_to_mysql():
    try:
        # Do not touch these settings
        connection = pymysql.connect(
            host='192.168.12.12',
            user='sixfold1',
            password='10312018',
            database='sixFold'
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def addingMovieToDB(movie_title, db):
    username = session.get('username', 'Guest')
    if username != 'Guest':
        connection = connect_to_mysql()
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM users WHERE username = %s;", (username,))
        user_id_row = cursor.fetchone()

        user_id = user_id_row[0] if user_id_row else None

        if user_id:
            cursor.execute(f"INSERT INTO {db} (user_id, movie_title) VALUES (%s, %s);", (user_id, movie_title))
            connection.commit()
            print(f"{movie_title} added to {db}")
        else:
            print("user not found")
        cursor.close()
        connection.close()

def getMovieInfoFromDB(db):
    username = session.get('username', 'Guest')
    if username != 'Guest':
        connection = connect_to_mysql()
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM users WHERE username = %s;", (username,))
        user_id_row = cursor.fetchone()

        user_id = user_id_row[0] if user_id_row else None

        if user_id:
            cursor.execute(f"SELECT movie_title FROM {db} WHERE user_id = %s", (user_id,))
            
            movie_results = cursor.fetchall()
            print(f"showing Movies from {db}")

            cursor.close()
            connection.close()
            
            return movie_results

        else:
            print("user not found")

        cursor.close()
        connection.close()

# Check on login HTML
@app.route('/')
def home():
    # Retrieve username from session or default to 'Guest'
    username = session.get('username', 'Guest')  
    return render_template('login.html', username=username)  # Render login form with username

@app.route('/login', methods=['POST', 'GET'])
def login():
    # Get form inputs
    username = request.form.get('username')  
    password = request.form.get('psw')  
    
    connection = connect_to_mysql()  # Your function to connect to the database
    if connection:
        cursor = connection.cursor()
        # Query to check if username and password match
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()  
        cursor.close()
        connection.close()

        if user:
            # Store the username in session
            session['username'] = username
            flash('Login successful!')

            # Check for a special user and render with appropriate image
            if session['username'] == "testuser":
                image_url = "https://media.tenor.com/ciegZ6-LGR4AAAAe/cool-link-shades.png"
            else:
                image_url = "static/images/Default_pfp.svg.png"

            # Render index.html with username and image URL
            return render_template('index.html', image_url=image_url, username=username)
        else:
            # Invalid credentials
            flash('Invalid username or password. Please try again.')
            return redirect(url_for('home'))  # Redirect to login page
    else:
        flash('Unable to connect to the database.')
        return redirect(url_for('home'))
@app.route('/logout')

def logout():
    # Remove the username from the session
    session.pop('username', None)
    flash('You have been logged out.')
    print("YOU LOGGED OUT")
    return redirect(url_for('home'))

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/results', methods=['POST','GET'])
def results():
    username = session.get('username', 'Guest')
    title = request.args.get("movieTitle")

    addingMovieToDB(title, "SearchHistory")

    key = "96ae5860"

    #setting up api to request info from api
    omdb.set_default('apikey', key)

    #will search all related movies with that title, you can include parameters like year, and other stuff (read doc)
    movies = omdb.search_movie(title)

    movie_details_list = []

    for movie in movies:
        movie_details = omdb.imdbid(movie['imdb_id'])
        movie_info = {
            'title': movie_details.get('title', 'Unknown Title'),
            'poster': movie_details.get('poster', 'N/A'),
            'ratings': movie_details.get('imdb_rating', 'N/A'),
            'plot': movie_details.get('plot', 'No synopsis available'),
            'imdb_url': f"https://www.imdb.com/title/{movie['imdb_id']}/",
            'related_movies_url': 'https://www.imdb.com/',  # Placeholder, imdb doesnt show related movies with api
            'showtimes_url': 'https://www.imdb.com/'  # Placeholder, they dont offer showtimes either via api
        }
        if movie_info['poster'] != "N/A":
            movie_details_list.append(movie_info)

    return render_template('results.html', movies=movie_details_list, username = username)

#hi

@app.route('/profile')
def profile():
    username = session.get('username', 'Guest')
    return render_template('profile.html', username = username)

@app.route('/settings')
def settings():
    username = session.get('username', 'Guest')
    return render_template('settings.html', username = username)

@app.route('/history')
def history():
    username = session.get('username', 'Guest')
    history = getMovieInfoFromDB("SearchHistory")

    # Pass the history to the template
    return render_template('history.html', history=history, username = username)

@app.route('/add-to-watchlist', methods=['POST', 'GET'])
def add_to_watchlist():
    data = request.get_json()  # Get the JSON data sent from the client
    movie_title = data.get('title')  # Extract the movie title

    addingMovieToDB(movie_title, "Watchlist")
    
    # Respond back to the client
    return jsonify({"message": f"Movie '{movie_title}' added to watchlist!"})


@app.route('/add-to-favorites', methods=['POST'])
def add_to_favorites():
    data = request.get_json()  # Get the JSON data sent from the client
    movie_title = data.get('title')  # Extract the movie title
    
    addingMovieToDB(movie_title, "FavoriteMovies")
    
    # Respond back to the client
    return jsonify({"message": f"Movie '{movie_title}' added to favorites!"})



@app.route('/register', methods=['POST', 'GET'])
def register_user():
    # Get info
    username = request.form.get('username')
    password = request.form.get('psw')
        
    # Make connection to database
    connection = connect_to_mysql()

    if connection:
        cursor = connection.cursor()
        insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(insert_query, (username, password))
        connection.commit()
        cursor.close()
        connection.close()
    
    return redirect(url_for('home'))


@app.route('/favorites')
def favorites():
    username = session.get('username', 'Guest')
    return render_template('favorites.html', username = username)

@app.route('/watchlist')
def watchlist():
    username = session.get('username', 'Guest')
    return render_template('watchlist.html', username = username)

if __name__ == "__main__":
    # Get the PORT environment variable or use a default port
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)

