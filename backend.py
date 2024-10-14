#pip install omdb in terminal
import omdb
from omdb import OMDBClient 
client = OMDBClient(apikey='96ae5860')
import string
string.letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
import random
randomid=("tt" +str(random.randint(1,9000000))) #Grab random IMDb ID
random.choice(string.ascii_letters) #Grab random first letter for searching (Currently doesn't work, exact matches of words included in a title are required)

def random_movie():
    roll = client.get(search="The Matrix") #Searches the given string in the API's movie catalog. Currently only searches exact matches.
    return roll

random_movie()