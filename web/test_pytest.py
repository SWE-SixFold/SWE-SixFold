# In terminal:
# python3 -m venv myenv
# iOS -source myenv/bin/activate
# Windows -source myenv\Scripts\activate
# pip install pytest
# cd web
# pytest
# deactivate (when youre done)

import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import omdb
omdb.set_default('apikey', '96ae5860')

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key


from app import results
import backend

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
    return None