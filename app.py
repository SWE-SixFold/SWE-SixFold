import pymysql
from flask import Flask, render_template, request, redirect, url_for, flash

#TODO duplicates

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

#connect to sql function

def connect_to_mysql():
    try:
        #do not touch these settings
        connection = pymysql.connect(
            host='10.0.0.43',
            user='sixfold',
            password='10312018',
            database='sixFold'
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

#check on login html

@app.route('/')
def home():
    return render_template('login.html')  # Render the login form



@app.route('/login', methods=['POST','GET'])
def login():
    username = request.form.get('username') # Get username from form
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
            # Successful login
            flash('Login successful!')
            return render_template('index.html')  # Redirect to home or dashboard
        else:
            # Invalid credentials
            flash('Invalid username or password. Please try again.')
            return redirect(url_for('home'))

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)
