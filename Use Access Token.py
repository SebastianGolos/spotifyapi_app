import requests
from BaseAPIClientClass import SpotifyAPI
from urllib.parse import urlencode
import pprint


client_id = '5f7f8ca9b4e34c248ea26ac960c5d3fd'
client_secret = 'ba28555b8772405dbba03b9f9e0dac77'

spotify = SpotifyAPI(client_id, client_secret)
# data = spotify.get_client_top_artists() 
data = spotify.get_client_top_tracks() 

# pprint.pprint(spotify.search({"track":"Ageispolis", "artist":"Aphex Twin"}, search_type="track"))

# print(spotify.base_search(urlencode({"q":"time", "type":"track"})))

# data = data['items']

# for element in data:
#     pprint.pprint(element['name'])
#     pprint.pprint(spotify.get_track(element['id']))


# print(spotify.get_track('38wCbVfMreML5ZhF5iQuKA'))
rec = spotify.get_recommendations('JP', '38wCbVfMreML5ZhF5iQuKA')
# pprint.pprint(rec['seeds'])
rec_data = rec['seeds']
rec_data2 = rec['tracks']
# print(rec_data2)

for element in rec_data2:
    print(element['name'])
    # print(element['artist'])

# for element in rec_data:
#     pprint.pprint(element['name'])
#     pprint.pprint(element['artist'])



 
