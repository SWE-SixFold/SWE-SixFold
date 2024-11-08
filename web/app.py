import os
import pymysql
from flask import Flask, render_template, request, redirect, url_for, flash, session
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
            host='10.250.87.64',
            user='sixfold',
            password='10312018',
            database='sixFold'
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

# Check on login HTML
@app.route('/')
def home():
    return render_template('login.html')  # Render the login form

@app.route('/login', methods=['POST', 'GET'])
def login():
    username = request.form.get('username')  # Get username from form
    password = request.form.get('psw')  # Get password from form
    
    connection = connect_to_mysql()
    if connection:
        cursor = connection.cursor()
        # Query to check if the username and password match
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()  # Fetch one matching record
        cursor.close()
        connection.close()

        if user:
            # Store username in session
            session['username'] = username
            flash('Login successful!')
            if session['username'] == "testuser":
                image_url = "https://media.tenor.com/ciegZ6-LGR4AAAAe/cool-link-shades.png"
                return render_template('index.html', image_url = image_url)  # Redirect to home or dashboard
            else:
                image_url = "static/images/Default_pfp.svg.png"
                return render_template('index.html', image_url = image_url)
        else:
            # Invalid credentials
            flash('Invalid username or password. Please try again.')
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

    title = request.args.get("movieTitle")

    key = "96ae5860"

    #setting up api to request info from api
    omdb.set_default('apikey', key)

    #will search all related movies with that title, you can include parameters like year, and other stuff (read doc)
    movies = omdb.search_movie(title)

    posters = []

    for movie in range(0, len(movies)):
        image = (movies[movie]['poster'])
        if image != "N/A":
            posters.append(image)

    return render_template('results.html', posters = posters)




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

if __name__ == "__main__":
    # Get the PORT environment variable or use a default port
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
