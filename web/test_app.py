# **CURRENTLY DATABASE ONLY WORKS LOCALLY, SO YOU MUST BE
# CONNECTED TO IT TO RUN THIS CODE!**

# In terminal:
# python3 -m venv myenv
# MAC OS -source myenv/bin/activate
# Windows -source myenv\Scripts\activate
# pip install pytest
# cd web
# on terminal run "pytest test_app.py"


import os
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import pymysql
import pymysql.cursors
import omdb
from app import app

def connect_to_mysql():
    try:
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

#Requirement 1
#test case ID: 1.1
def test_login():
    username = "testuser"
    password = "testpassword"

    connection = connect_to_mysql()

    if connection:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()  
        cursor.close()
        connection.close()

        assert user
        print(f"Log in successful for {username}")

#test case ID: 1.2
def test_login_wrong_credentials():
    username = "wronguser"
    password = "wrongpassword"

    connection = connect_to_mysql()

    if connection:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()  
        cursor.close()
        connection.close()

        assert not user

#Requirement 5
#test case ID: 5.1
def test_search_existing_movie():
    omdb.set_default('apikey', '96ae5860')

    test_search_keyword = "Home alone"

    movie = omdb.search_movie(test_search_keyword)
    
    assert movie

#test case ID: 5.2
def test_movie_details():
    omdb.set_default('apikey', "96ae5860")

    movies = omdb.search_movie("Home alone")

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

    assert movie_details

#test case ID: 5.3
def test_search_nonexisting_movie():
    omdb.set_default('apikey', '96ae5860')

    test_search_keyword = ""

    movie = omdb.search_movie(test_search_keyword)
    
    if not test_search_existing_movie:
        print("No movies match your keyword")

    assert not movie

#Requirement 11

#requirement 11.1
def test_add_to_Favs():
    user_id = 1
    movie_id = "testID"

    connection = connect_to_mysql()

    if connection:
        cursor = connection.cursor()

        cursor.execute(f"INSERT INTO FavoriteMovies (user_id, movie_id) VALUES (%s, %s);", (user_id, movie_id))
        connection.commit()
        cursor.execute("SELECT EXISTS(SELECT 1 FROM FavoriteMovies WHERE user_id = %s AND movie_id = %s)", (user_id, movie_id))
        result = cursor.fetchone()  

        assert result[0] == 1

        cursor.execute("DELETE FROM FavoriteMovies WHERE user_id = %s AND movie_id = %s;", (user_id, movie_id))
        connection.commit()

        cursor.close()
        connection.close()

#Requirement 12

#Test case ID: 12.1
def test_show_favs():
    user_id = 1

    connection = connect_to_mysql()

    if connection:
        cursor = connection.cursor()

        cursor.execute(f"SELECT movie_id FROM FavoriteMovies WHERE user_id = %s", (user_id,))
        movie_results = cursor.fetchall()
        print(movie_results)
        cursor.close()
        connection.close()
        for i in movie_results:
            print(i)
    assert movie_results

#Requirement 18

#Test case ID: 18.1
def test_add_to_Watchlist():
    user_id = 1
    movie_title = "movie_title"

    connection = connect_to_mysql()

    if connection:
        cursor = connection.cursor()

        cursor.execute(f"INSERT INTO Watchlist (user_id, movie_title) VALUES (%s, %s);", (user_id, movie_title))
        connection.commit()
        cursor.execute("SELECT EXISTS(SELECT 1 FROM Watchlist WHERE user_id = %s AND movie_title = %s)", (user_id, movie_title))
        result = cursor.fetchone()  

        assert result[0] == 1

        cursor.execute("DELETE FROM Watchlist WHERE user_id = %s AND movie_title = %s;", (user_id, movie_title))
        connection.commit()

        cursor.close()
        connection.close()


'''
# Login Testing
# 1.1 - Successful Login
def test_login():
    return None

# 1.2 - Failed Login
def test_login_fail():
    return None

# 1.3 - Logout
def test_logout():
    return None
# 1.4 - Transmission to Dashboard
def test_transmission():
    return None

# Searchbar Testing
# 5.1 - Keyword Search
def test_keyword():
    keyword = "Home Alone" #Example Movie Title
    assert type(omdb.search_movie(keyword)) == list, "False"

# 5.2 - Search Result Display
def test_search_display():
    assert results() #Test for the results.html url generated using an example keyword

# 5.3 - No Results Display
def test_search_nomatch():
    assert results() #Test to make sure throwing a keyword with no matches returns no results

# 5.4 - Force Login (Are we keeping this?)
def test_loginsearch():
    return None

# Favorites Testing
# 12.1 - Favorite List View
def test_view_favorites():
    return None

# 12.2 - Clear Favorite List
def test_clear_favorites():
    return None

# Watchlist Testing
# 18.1 - Save Movies to Watchlist
def test_save_watchlist():
    return None

# 18.2 - Clear Watchlist
def test_clear_watchlist():
    return None'''