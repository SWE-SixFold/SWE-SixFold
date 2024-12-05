import os
import pymysql
import socket
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import pymysql.cursors
import omdb

"""
TODO 
    notes
    bio?
    update username and passwords?
    recommended????
"""

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Connect to SQL function
def connect_to_mysql():
    try:
        # Do not touch these settings
        connection = pymysql.connect(
            host= socket.gethostbyname(socket.gethostname()), #gets local ip address
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
    
    # Check if the user is logged in
    if username != 'Guest':
        connection = connect_to_mysql()
        cursor = connection.cursor()

        # Get user_id from the username
        cursor.execute("SELECT id FROM users WHERE username = %s;", (username,))
        user_id_row = cursor.fetchone()
        user_id = user_id_row[0] if user_id_row else None

        if user_id:
            # Check if the movie already exists in the database for the user
            cursor.execute(f"SELECT 1 FROM {db} WHERE user_id = %s AND movie_title = %s LIMIT 1;", (user_id, movie_title))
            existing_movie = cursor.fetchone()

            if existing_movie:
                print(f"{movie_title} already exists in the {db} for the user.")
            else:
                # Insert the movie if it doesn't exist
                cursor.execute(f"INSERT INTO {db} (user_id, movie_title) VALUES (%s, %s);", (user_id, movie_title))
                connection.commit()
                print(f"{movie_title} added to {db}.")
        else:
            print("User not found.")
        
        cursor.close()
        connection.close()
    else:
        print("User is not logged in.")

def addingMovieID_ToDB(movie_id, db):
    username = session.get('username', 'Guest')
    if username != 'Guest':
        connection = connect_to_mysql()
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM users WHERE username = %s;", (username,))
        user_id_row = cursor.fetchone()

        user_id = user_id_row[0] if user_id_row else None

        if user_id:
            cursor.execute(f"INSERT INTO {db} (user_id, movie_id) VALUES (%s, %s);", (user_id, movie_id))
            connection.commit()
            print(f"{movie_id} added to {db}")
        else:
            print("user not found")
        cursor.close()
        connection.close()

def clear_movies_from_db(db):
    username = session.get('username', 'Guest')  # Correct method is 'get'

    if username == 'Guest':
        flash("You must be logged in to perform this action.", "error")
        return render_template("profile.html")
    
    connection = connect_to_mysql()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s;", (username,))
        user_id_row = cursor.fetchone()
        user_id = user_id_row[0] if user_id_row else None

        # Delete movies for the given user_id
        cursor.execute(f"DELETE FROM {db} WHERE user_id = %s", (user_id,))
        connection.commit()  # Commit the transaction to apply changes
        flash("Your movies have been cleared!", "success")
        cursor.close()
        connection.close()

def getMovieTitleInfoFromDB(db):
    username = session.get('username', 'Guest')
    # Return preloaded movies_data for Guest user
    if username == 'Guest':
        movies_data = [
        {
            "Title": "Home Alone",
            "Poster": "https://m.media-amazon.com/images/M/MV5BNzNmNmQ2ZDEtMTc1MS00NjNiLThlMGUtZmQxNTg1Nzg5NWMzXkEyXkFqcGc@._V1_SX300.jpg",
            "IMDb Rating": "7.7",
            "Plot": "An eight-year-old troublemaker, mistakenly left home alone, must defend his home against a pair of burglars on Christmas Eve.",
            "IMDb URL": "https://www.imdb.com/title/tt0099785/",
            "Related Movies URL": "https://www.imdb.com/",
            "Showtimes URL": "https://www.imdb.com/"
        },
        {
            "Title": "Home Alone 2: Lost in New York",
            "Poster": "https://m.media-amazon.com/images/M/MV5BOGEyYzRmNzYtYzJjZi00ZjhlLWJiNDktYzZhNTgxMzc1NThlXkEyXkFqcGc@._V1_SX300.jpg",
            "IMDb Rating": "6.9",
            "Plot": "Kevin accidentally boards a flight to New York City and gets separated from his family who are on their way to Miami. He then bumps into two of his old enemies, who plan to rob a toy store.",
            "IMDb URL": "https://www.imdb.com/title/tt0104431/",
            "Related Movies URL": "https://www.imdb.com/",
            "Showtimes URL": "https://www.imdb.com/"
        },
        {
            "Title": "Home Alone 3",
            "Poster": "https://m.media-amazon.com/images/M/MV5BNmI0MjcxYjYtYzY5Ni00NjBkLTllN2MtZGYyNzJiYzA5ZGYxXkEyXkFqcGc@._V1_SX300.jpg",
            "IMDb Rating": "4.6",
            "Plot": "Alex Pruitt, an 8-year-old boy living in Chicago, must fend off international spies who seek a top-secret computer chip in his toy car.",
            "IMDb URL": "https://www.imdb.com/title/tt0119303/",
            "Related Movies URL": "https://www.imdb.com/",
            "Showtimes URL": "https://www.imdb.com/"
        },
        {
            "Title": "Home Alone 4: Taking Back the House",
            "Poster": "https://m.media-amazon.com/images/M/MV5BZGZmNDUzOWMtZWRjMC00NjRkLTkyNjQtMDA4YWNhZWY4NjI3XkEyXkFqcGc@._V1_SX300.jpg",
            "IMDb Rating": "2.6",
            "Plot": "Amidst his parents' impending divorce, Kevin McCallister must foil his old nemesis Marv and his wife Vera's plot to kidnap a Crown Prince.",
            "IMDb URL": "https://www.imdb.com/title/tt0329200/",
            "Related Movies URL": "https://www.imdb.com/",
            "Showtimes URL": "https://www.imdb.com/"
        },
        {
            "Title": "A Girl Walks Home Alone at Night",
            "Poster": "https://m.media-amazon.com/images/M/MV5BMjMzNjMyMjU2M15BMl5BanBnXkFtZTgwMzA3NjQ0MzE@._V1_SX300.jpg",
            "IMDb Rating": "6.9",
            "Plot": "In the Iranian ghost-town Bad City, a place that reeks of death and loneliness, the townspeople are unaware they are being stalked by a lonesome vampire.",
            "IMDb URL": "https://www.imdb.com/title/tt2326554/",
            "Related Movies URL": "https://www.imdb.com/",
            "Showtimes URL": "https://www.imdb.com/"
        },
        {
            "Title": "Home Sweet Home Alone",
            "Poster": "https://m.media-amazon.com/images/M/MV5BODQ4NjUxZmItNGNlZC00ZGI1LWEyNDYtZjg5ZTk0ZGU5MTlhXkEyXkFqcGc@._V1_SX300.jpg",
            "IMDb Rating": "3.6",
            "Plot": "A married couple tries to steal back a valuable heirloom from a troublesome kid.",
            "IMDb URL": "https://www.imdb.com/title/tt11012066/",
            "Related Movies URL": "https://www.imdb.com/",
            "Showtimes URL": "https://www.imdb.com/"
        },
        {
            "Title": "Home Alone: The Holiday Heist",
            "Poster": "https://m.media-amazon.com/images/M/MV5BYWUxNGM0MWUtMGZjNi00ODQwLWFlM2ItMzVlMWFhNDE0MGRiXkEyXkFqcGc@._V1_SX300.jpg",
            "IMDb Rating": "3.5",
            "Plot": "Finn Baxter sets up booby traps to catch the ghost of his new home's former occupant, then discovers that he must protect the house and his sister from three bumbling art thieves.",
            "IMDb URL": "https://www.imdb.com/title/tt2308733/",
            "Related Movies URL": "https://www.imdb.com/",
            "Showtimes URL": "https://www.imdb.com/"
        },
        {
            "Title": "Home Alone 4",
            "Poster": "https://m.media-amazon.com/images/M/MV5BOGFlNjMyOTYtNjRkZi00MTljLTgyN2EtNDQ5MjFlMmZkNDJiXkEyXkFqcGdeQXVyMzc5MTE4NzY@._V1_SX300.jpg",
            "IMDb Rating": "2.8",
            "Plot": "Kevin McCallister travels to his father over Christmas and must defend the house against old enemies who plan to kidnap the Crown Prince.",
            "IMDb URL": "https://www.imdb.com/title/tt13677540/",
            "Related Movies URL": "https://www.imdb.com/",
            "Showtimes URL": "https://www.imdb.com/"
        },
        {
            "Title": "Google Assistant: Home Alone Again",
            "Poster": "https://m.media-amazon.com/images/M/MV5BOWFkZGYxZjUtMmNlMi00NzYxLWI0M2EtYmY2ZDA5YmMyMDE3XkEyXkFqcGdeQXVyNDE5MTU2MDE@._V1_SX300.jpg",
            "IMDb Rating": "8.3",
            "Plot": "The ad follows a similar plot to the Christmas comedy, with Culkin waking up in an empty house alone - except for his Google Assistant, of course.",
            "IMDb URL": "https://www.imdb.com/title/tt9493634/",
            "Related Movies URL": "https://www.imdb.com/",
            "Showtimes URL": "https://www.imdb.com/"
        },
        {
            "Title": "Home, Not Alone",
            "Poster": "https://m.media-amazon.com/images/M/MV5BOGU0NDQ2MTEtYmNlZS00MTFkLWE2M2ItZGE2OWFlYmQ2OWUyXkEyXkFqcGc@._V1_SX300.jpg",
            "IMDb Rating": "4.4",
            "Plot": "Sara and her 18-year-old daughter Jordyn find their dream home in a beautiful neighborhood, only to discover that the house's former owner refuses to let go of the property.",
            "IMDb URL": "https://www.imdb.com/title/tt26458500/",
            "Related Movies URL": "https://www.imdb.com/",
            "Showtimes URL": "https://www.imdb.com/"
        }
    ]

        print(f"Guest user viewing {db}. Showing preloaded data.")
        return movies_data  # Use preloaded data for Guest

    connection = connect_to_mysql()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s;", (username,))
        user_id_row = cursor.fetchone()
        user_id = user_id_row[0] if user_id_row else None

        if user_id:
            cursor.execute(f"SELECT movie_title FROM {db} WHERE user_id = %s", (user_id,))
            movie_results = cursor.fetchall()
            cursor.close()
            connection.close()
            return movie_results
        else:
            cursor.close()
            connection.close()
            print("User not found in database.")
    return []

def getMovieIDInfoFromDB(db):

    movies_data = [
    {
        "Title": "Home Alone",
        "Poster": "https://m.media-amazon.com/images/M/MV5BNzNmNmQ2ZDEtMTc1MS00NjNiLThlMGUtZmQxNTg1Nzg5NWMzXkEyXkFqcGc@._V1_SX300.jpg",
        "IMDb Rating": "7.7",
        "Plot": "An eight-year-old troublemaker, mistakenly left home alone, must defend his home against a pair of burglars on Christmas Eve.",
        "IMDb URL": "https://www.imdb.com/title/tt0099785/",
        "Related Movies URL": "https://www.imdb.com/",
        "Showtimes URL": "https://www.imdb.com/"
    },
    {
        "Title": "Home Alone 2: Lost in New York",
        "Poster": "https://m.media-amazon.com/images/M/MV5BOGEyYzRmNzYtYzJjZi00ZjhlLWJiNDktYzZhNTgxMzc1NThlXkEyXkFqcGc@._V1_SX300.jpg",
        "IMDb Rating": "6.9",
        "Plot": "Kevin accidentally boards a flight to New York City and gets separated from his family who are on their way to Miami. He then bumps into two of his old enemies, who plan to rob a toy store.",
        "IMDb URL": "https://www.imdb.com/title/tt0104431/",
        "Related Movies URL": "https://www.imdb.com/",
        "Showtimes URL": "https://www.imdb.com/"
    },
    {
        "Title": "Home Alone 3",
        "Poster": "https://m.media-amazon.com/images/M/MV5BNmI0MjcxYjYtYzY5Ni00NjBkLTllN2MtZGYyNzJiYzA5ZGYxXkEyXkFqcGc@._V1_SX300.jpg",
        "IMDb Rating": "4.6",
        "Plot": "Alex Pruitt, an 8-year-old boy living in Chicago, must fend off international spies who seek a top-secret computer chip in his toy car.",
        "IMDb URL": "https://www.imdb.com/title/tt0119303/",
        "Related Movies URL": "https://www.imdb.com/",
        "Showtimes URL": "https://www.imdb.com/"
    },
    {
        "Title": "Home Alone 4: Taking Back the House",
        "Poster": "https://m.media-amazon.com/images/M/MV5BZGZmNDUzOWMtZWRjMC00NjRkLTkyNjQtMDA4YWNhZWY4NjI3XkEyXkFqcGc@._V1_SX300.jpg",
        "IMDb Rating": "2.6",
        "Plot": "Amidst his parents' impending divorce, Kevin McCallister must foil his old nemesis Marv and his wife Vera's plot to kidnap a Crown Prince.",
        "IMDb URL": "https://www.imdb.com/title/tt0329200/",
        "Related Movies URL": "https://www.imdb.com/",
        "Showtimes URL": "https://www.imdb.com/"
    },
    {
        "Title": "A Girl Walks Home Alone at Night",
        "Poster": "https://m.media-amazon.com/images/M/MV5BMjMzNjMyMjU2M15BMl5BanBnXkFtZTgwMzA3NjQ0MzE@._V1_SX300.jpg",
        "IMDb Rating": "6.9",
        "Plot": "In the Iranian ghost-town Bad City, a place that reeks of death and loneliness, the townspeople are unaware they are being stalked by a lonesome vampire.",
        "IMDb URL": "https://www.imdb.com/title/tt2326554/",
        "Related Movies URL": "https://www.imdb.com/",
        "Showtimes URL": "https://www.imdb.com/"
    },
    {
        "Title": "Home Sweet Home Alone",
        "Poster": "https://m.media-amazon.com/images/M/MV5BODQ4NjUxZmItNGNlZC00ZGI1LWEyNDYtZjg5ZTk0ZGU5MTlhXkEyXkFqcGc@._V1_SX300.jpg",
        "IMDb Rating": "3.6",
        "Plot": "A married couple tries to steal back a valuable heirloom from a troublesome kid.",
        "IMDb URL": "https://www.imdb.com/title/tt11012066/",
        "Related Movies URL": "https://www.imdb.com/",
        "Showtimes URL": "https://www.imdb.com/"
    },
    {
        "Title": "Home Alone: The Holiday Heist",
        "Poster": "https://m.media-amazon.com/images/M/MV5BYWUxNGM0MWUtMGZjNi00ODQwLWFlM2ItMzVlMWFhNDE0MGRiXkEyXkFqcGc@._V1_SX300.jpg",
        "IMDb Rating": "3.5",
        "Plot": "Finn Baxter sets up booby traps to catch the ghost of his new home's former occupant, then discovers that he must protect the house and his sister from three bumbling art thieves.",
        "IMDb URL": "https://www.imdb.com/title/tt2308733/",
        "Related Movies URL": "https://www.imdb.com/",
        "Showtimes URL": "https://www.imdb.com/"
    },
    {
        "Title": "Home Alone 4",
        "Poster": "https://m.media-amazon.com/images/M/MV5BOGFlNjMyOTYtNjRkZi00MTljLTgyN2EtNDQ5MjFlMmZkNDJiXkEyXkFqcGdeQXVyMzc5MTE4NzY@._V1_SX300.jpg",
        "IMDb Rating": "2.8",
        "Plot": "Kevin McCallister travels to his father over Christmas and must defend the house against old enemies who plan to kidnap the Crown Prince.",
        "IMDb URL": "https://www.imdb.com/title/tt13677540/",
        "Related Movies URL": "https://www.imdb.com/",
        "Showtimes URL": "https://www.imdb.com/"
    },
    {
        "Title": "Google Assistant: Home Alone Again",
        "Poster": "https://m.media-amazon.com/images/M/MV5BOWFkZGYxZjUtMmNlMi00NzYxLWI0M2EtYmY2ZDA5YmMyMDE3XkEyXkFqcGdeQXVyNDE5MTU2MDE@._V1_SX300.jpg",
        "IMDb Rating": "8.3",
        "Plot": "The ad follows a similar plot to the Christmas comedy, with Culkin waking up in an empty house alone - except for his Google Assistant, of course.",
        "IMDb URL": "https://www.imdb.com/title/tt9493634/",
        "Related Movies URL": "https://www.imdb.com/",
        "Showtimes URL": "https://www.imdb.com/"
    },
    {
        "Title": "Home, Not Alone",
        "Poster": "https://m.media-amazon.com/images/M/MV5BOGU0NDQ2MTEtYmNlZS00MTFkLWE2M2ItZGE2OWFlYmQ2OWUyXkEyXkFqcGc@._V1_SX300.jpg",
        "IMDb Rating": "4.4",
        "Plot": "Sara and her 18-year-old daughter Jordyn find their dream home in a beautiful neighborhood, only to discover that the house's former owner refuses to let go of the property.",
        "IMDb URL": "https://www.imdb.com/title/tt26458500/",
        "Related Movies URL": "https://www.imdb.com/",
        "Showtimes URL": "https://www.imdb.com/"
    }
]

    key = "96ae5860"

    # Setting up API to request info from OMDB
    omdb.set_default('apikey', key)

    username = session.get('username', 'Guest')
    # Return preloaded movies_data for Guest user
    if username == 'Guest':
        print(f"Guest user viewing {db}. Showing preloaded data.")
        return movies_data  # Use preloaded data for Guest

    connection = connect_to_mysql()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s;", (username,))
        user_id_row = cursor.fetchone()
        user_id = user_id_row[0] if user_id_row else None

        if user_id:
            cursor.execute(f"SELECT movie_id FROM {db} WHERE user_id = %s", (user_id,))
            movie_results = cursor.fetchall()
            cursor.close()
            connection.close()

            movie_ids = [row[0] for row in movie_results]

            movies_data = []

            for id in movie_ids:
                # Fetch movie details from OMDB
                movie_details = omdb.imdbid(id)
                
                # Format movie details
                formatted_movie = {
                    "Title": movie_details.get("title"),
                    "Poster": movie_details.get("poster"),
                    "IMDb Rating": movie_details.get("imdb_rating"),
                    "Plot": movie_details.get("plot"),
                    "IMDb URL": f"https://www.imdb.com/title/{movie_details.get('imdb_id')}/",
                    "Related Movies URL": "https://www.imdb.com/",
                    "Showtimes URL": "https://www.imdb.com/"
                }

                movies_data.append(formatted_movie)

            return movies_data
        else:
            cursor.close()
            connection.close()
            print("User not found in database.")
    return []

def getNotes():
    username = session.get('username', 'Guest')
    # Return preloaded movies_data for Guest user
    if username == 'Guest':
        notes = (("Home alone", "Amazing movie", "date"), ("The Grinch", "Cool xmas movie!", "date"))
        return notes  # Use preloaded data for Guest

    connection = connect_to_mysql()
    cursor = connection.cursor()

    if connection:
        
        cursor.execute("SELECT id FROM users WHERE username = %s;", (username,))
        user_id_row = cursor.fetchone()
        user_id = user_id_row[0] if user_id_row else None

        if user_id:
            cursor.execute("SELECT movie_title, note, created_at FROM MovieNotes WHERE user_id = %s", (user_id,))
            notes = cursor.fetchall()

            #note[0] = movie title
            #note[1] = movie note
            #note[3] = date taken

            cursor.close()
            connection.close()

            return notes

def getHistory(db):
        movies_data = ["Home alone", "Transformers", "Georgia State"]

        key = "96ae5860"

        # Setting up API to request info from OMDB
        omdb.set_default('apikey', key)

        username = session.get('username', 'Guest')
        # Return preloaded movies_data for Guest user
        if username == 'Guest':
            print(f"Guest user viewing {db}. Showing preloaded data.")
            return movies_data  # Use preloaded data for Guest

        connection = connect_to_mysql()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM users WHERE username = %s;", (username,))
            user_id_row = cursor.fetchone()
            user_id = user_id_row[0] if user_id_row else None

            if user_id:
                cursor.execute(f"SELECT movie_title FROM {db} WHERE user_id = %s", (user_id,))
                movie_results = cursor.fetchall()
                cursor.close()
                connection.close()

                movie_titles = [row[0] for row in movie_results]
                print(movie_titles)
                return movie_titles
            else:
                cursor.close()
                connection.close()
                print("User not found in database.")
        return []

# Check on login HTML
@app.route('/')
def home():

    api_key_tmdb = "70650a90bf3d2a8c14f055326a191bbe"
    image_base_url = "https://image.tmdb.org/t/p/w500"

    # Check if the user is logged in
    #if 'username' not in session:
        #return redirect('/login')  # Redirect to the login page

    username = session.get('username', 'Guest')
    watchlist_movies = getMovieIDInfoFromDB("Watchlist")[:3]
    
    # Fetch the current movies playing in theaters
    url = f'https://api.themoviedb.org/3/movie/now_playing?api_key={api_key_tmdb}&language=en-US&page=1'

    response = requests.get(url)
    now_playing = response.json()

    # Prepare a list of movies to pass to the template
    theater_movies = []
    for movie in now_playing['results'][:5]:
        title = movie['title']
        poster_path = movie['poster_path']
        movie_id = movie['id']
        tmdb_link = f"https://www.themoviedb.org/movie/{movie_id}"
        poster_url = f"{image_base_url}{poster_path}" if poster_path else None

        theater_movies.append({
            'title': title,
            'poster_url': poster_url,
            'tmdb_link': tmdb_link
        })

    return render_template('index.html', username=username, watchlist=watchlist_movies, theater_movies=theater_movies)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':  # Handle form submission
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

                # Redirect to the home page where the `watchlist` is properly handled
                return redirect(url_for('home'))
            else:
                # Invalid credentials
                flash('Invalid username or password. Please try again.')
                return redirect(url_for('login'))  # Stay on the login page
        else:
            flash('Unable to connect to the database.')
            return redirect(url_for('login'))  # Stay on the login page
    
    # Render login.html for GET requests
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Remove the username from the session
    session.pop('username', None)
    flash('You have been logged out.')
    print("YOU LOGGED OUT")
    return redirect(url_for('login'))

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
            'showtimes_url': 'https://www.imdb.com/',  # Placeholder, they dont offer showtimes either via api
            'imdb_id': movie['imdb_id']
        }
        if movie_info['poster'] != "N/A":
            movie_details_list.append(movie_info)

    return render_template('results.html', movies=movie_details_list, username = username)

@app.route('/profile')
def profile():
    watchlist_movies = getMovieIDInfoFromDB("Watchlist")
    favorite_movies = getMovieIDInfoFromDB("FavoriteMovies")
    notes = getNotes()

    username = session.get('username', 'Guest')
    return render_template('profile.html', username = username, watchlist = watchlist_movies, favorites = favorite_movies, notes = notes)

@app.route('/settings')
def settings():
    username = session.get('username', 'Guest')
    return render_template('settings.html', username = username)

#TODO also need to add imdb_id to database

@app.route('/history')
def history():
    username = session.get('username', 'Guest')
    historyDB = getHistory("SearchHistory")
    print(historyDB)
    return render_template('history.html', historyDB=historyDB, username=username)

@app.route('/add-to-watchlist', methods=['POST', 'GET'])
def add_to_watchlist():
    data = request.get_json()  # Get the JSON data sent from the client
    movie_id = data.get('imdb_id')  # Extract the movie title

    addingMovieID_ToDB(movie_id, "Watchlist")
    
    # Respond back to the client
    return jsonify({"message": f"Movie '{movie_id}' added to watchlist!"})

@app.route('/add-to-favorites', methods=['POST'])
def add_to_favorites():
    data = request.get_json()  # Get the JSON data sent from the client
    movie_id = data.get('imdb_id')  # Extract the movie title
    
    addingMovieID_ToDB(movie_id, "FavoriteMovies")
    
    # Respond back to the client
    return jsonify({"message": f"Movie Title = {data.get('title')} '{movie_id}' added to favorites!"})

@app.route('/save_note', methods=['POST'])
def save_note():
    # Get JSON data sent from the client
    data = request.get_json()
    movie_title = data.get('movie_title', '').strip()  # Extract the movie title
    note_text = data.get('note', '').strip()  # Extract the note text

    # Get the username from the session
    username = session.get('username', 'Guest')

    # Validate the data
    if username != 'Guest' and movie_title and note_text:
        connection = connect_to_mysql()
        cursor = connection.cursor()

        # Get user_id from the username
        cursor.execute("SELECT id FROM users WHERE username = %s;", (username,))
        user_id_row = cursor.fetchone()
        user_id = user_id_row[0] if user_id_row else None

        if user_id:
            # Insert the note into the MovieNotes table
            cursor.execute("INSERT INTO MovieNotes (user_id, movie_title, note) VALUES (%s, %s, %s);", (user_id, movie_title, note_text))
            connection.commit()

            # Print the note and movie title to the terminal
            print(f"Note from {username}: Movie - {movie_title}, Note - {note_text}")
            
            cursor.close()
            connection.close()

            # Return success response
            return jsonify({'status': 'success', 'message': 'Note saved.'})

    # Return error if validation fails
    return jsonify({'status': 'error', 'message': 'Movie title or note is invalid.'})

@app.route('/clear-watchlist', methods=['POST'])
def clear_watchlist():
    clear_movies_from_db("Watchlist")
    return redirect(url_for("profile"))

@app.route('/clear-favorites', methods=['POST'])
def clear_favorites():
    clear_movies_from_db("FavoriteMovies")
    return redirect(url_for("profile"))

#not needed since its on profile now
@app.route('/watchlist')
def watchlist():
    username = session.get('username', 'Guest')
    watchListDB = getMovieIDInfoFromDB("Watchlist")  # Fetch Watchlist data
    return render_template('watchlist.html', watchlistDB=watchListDB, username=username)
    
@app.route('/similar')
def similar():
    return render_template('similar.html')

@app.route('/noresults')
def noresults():
    return render_template('noresults.html')

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


#not needed since its on profile now
@app.route('/favorites')
def favorites():
    username = session.get('username', 'Guest')
    favoritesDB = getMovieIDInfoFromDB("FavoriteMovies")  # Fetch Favorites data
    print(favoritesDB)
    return render_template('favorites.html', favoritesDB=favoritesDB, username=username)

if __name__ == "__main__":
    # Get the PORT environment variable or use a default port
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)