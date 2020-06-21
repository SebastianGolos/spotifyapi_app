import requests
from BaseAPIClientClass import SpotifyAPI
from urllib.parse import urlencode
import pprint


client_id = '5f7f8ca9b4e34c248ea26ac960c5d3fd'
client_secret = 'ba28555b8772405dbba03b9f9e0dac77'

spotify = SpotifyAPI(client_id, client_secret)

# pprint.pprint(spotify.search("Ageispolis", search_type="track"))

# print(pprint.pprint(spotify.get_artist("6mrSUibBDyh1jdKw7bwcOK")))




 
