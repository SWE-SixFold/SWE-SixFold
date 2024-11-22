# to run use terminal in this order
# python3 -m venv myenv
# iOS -source myenv/bin/activate
# Windows -source myenv\Scripts\activate
#
# deactivate (when youre done)

from flask import Flask, render_template, jsonify, redirect, url_for
import omdb
import random

app = Flask(__name__)

# set up OMDb API key
omdb.set_default('apikey', '96ae5860')

# route to render the main page
@app.route('/')
def home():
    return render_template('index.html')

# route to handle the random movie functionality
@app.route('/random-movie')
def random_movie():
    # generate a random IMDb ID and fetch movie data
    idnum = random.randint(1000000, 9999999)
    random_id = f"tt{idnum}"
    try:
        movie = omdb.imdbid(random_id, timeout=3)
        if movie:
            return jsonify(movie)
    except:
        pass  # try another ID if there's a timeout or error

    # fallback if no valid movie is found
    return jsonify({'error': 'Movie not found, try again!'})

if __name__ == '__main__':
    app.run(debug=True)