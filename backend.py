#pip install omdb in terminal
import omdb
omdb.set_default('apikey', '96ae5860')
from omdb import OMDBClient
client = OMDBClient(apikey='96ae5860')
import random

def random_movieid(): #OMDb does not have a random movie method, so the ID might result in a timeout
    idnum = random.randint(1000000,9999999) #Generate random number
    randomid=("tt" +str(idnum)) #Create random IMDb ID
    roll = omdb.imdbid(randomid, timeout=3) #Searches the randomly generated ID in the database.
    return roll

def view_movie(title: str): #Enter a movie title to get a dictionary of specific information of the movie
    searchlist = omdb.search_movie(title, page=1)
    specific = searchlist[1]
    usedid = specific.get('imdb_id')
    details = omdb.imdbid(usedid, timeout=3)
    return details

case6 = random_movieid()
case9 = view_movie("The Matrix")

print(case6)
print(case9)
