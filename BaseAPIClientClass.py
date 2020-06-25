import base64
import datetime
import requests
from urllib.parse import urlencode

class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"
    
    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
    
    def get_client_credentials(self):
        """
        returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        
        return client_creds_b64.decode()


    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}",
        }

    def get_token_data(self):
        return {
            "grant_type": "client_credentials",  
            "scope": "user-top-read user-follow-read"          
        }

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()

        r = requests.post(token_url, data=token_data, headers=token_headers)

        # print(r.json())

        if r.status_code not in range(200, 299):
            return Exception("Could not autheticate.")

        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in']
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now 
        return True
    
    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token() 
        return token

    def base_search(self, query_params):
        endpoint = "https://api.spotify.com/v1/search"
        
        headers = self.get_resource_header()
        lookup_url = f"{endpoint}?{query_params}"
        r = requests.get(lookup_url, headers=headers)

        if r.status_code not in range(200, 299):
            return {}

        return r.json()
    
    #Operator query has to match type e.g. Artist and NOT Artist, not do Artist and NOT Song 
    def search(self, query=None, operator = None, operator_query = None, search_type = "artist"):
        if query == None:
            raise Exception("A query is required")
        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k,v in query.items()])
        if operator != None and operator_query != None:
            if operator.lower() == "or" or operator.lower() == "not":
                operator = operator.upper()
            if isinstance(operator_query, str):
                query = f"{query} {operator} {operator_query}"
        query_params = urlencode({"q": query, "type":search_type.lower()})
        print(query_params)
        return self.base_search(query_params)
        
    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}",
        }
        return headers

    def get_resource(self, lookup_id, resource_type='albums', version='v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()
    
    def get_album(self, _id):
        return self.get_resource(_id, resource_type='albums')
    
    def get_artist(self, _id):
        return self.get_resource(_id, resource_type='artists')

    def get_track(self, _id):
        endpoint = f"https://api.spotify.com/v1/audio-features/{_id}"
        headers = self.get_resource_header()
        
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        
        return r.json()
    
    # def get_recommendations(self, instrumentalness, key, liveness, loundness, mode, speechiness, tempo, time_signature, valence):
    def get_recommendations(self, market, tracks):
        headers = self.get_resource_header()
        query_params = urlencode({"market": market, "seed_tracks":tracks})
        endpoint = f"https://api.spotify.com/v1/recommendations?{query_params}"
        
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}

        
        return r.json()

    #Two functions below currently require manual input of bearer keys from web app interface
    def get_client_top_artists(self):
        endpoint = "https://api.spotify.com/v1/me/top/artists?time_range=medium_term&limit=10&offset=5"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            print(r.status_code)
            
            return {}
        return r.json()

    def get_client_top_tracks(self):
        endpoint = "https://api.spotify.com/v1/me/top/tracks?time_range=medium_term&limit=10&offset=5"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            print(r.status_code)
            return {}
        return r.json()
    