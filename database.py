import sqlite3

# Connect to the SQLite database
# This will create 'user.db' if it doesn't exist
conn = sqlite3.connect('user.db')

# Create a cursor object
cursor = conn.cursor()

# Create the users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    favorite_movie TEXT,
    movie_notes TEXT
)
''')

# Commit the changes
conn.commit()

# Function to add a user to the database
def add_user(username, password, favorite_movie, movie_notes):
    cursor.execute('''
    INSERT INTO users (username, password, favorite_movie, movie_notes)
    VALUES (?, ?, ?, ?)
    ''', (username, password, favorite_movie, movie_notes))
    conn.commit()

# Example of adding a user
add_user('john_doe', 'securepassword', 'Inception', 'Loved the plot twists!')

# Close the connection
conn.close()

print("Database created and user added successfully.")
