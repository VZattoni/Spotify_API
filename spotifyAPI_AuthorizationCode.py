from http import client
from pydoc import cli
import requests
import base64
import urllib.parse as urlparse
import datetime
import GenerateStr
import webbrowser

client_id = "2322de2d2edb44488cac8d73c3dd6af1"
client_secret = "3a035500fa614f0fa05015f1eda1e839"

class Spotify(object):

    def __init__(self, client_id, client_secret):   
        self.client_id = client_id
        self.client_secret = client_secret
    

    def get_authorization_code(self):

        redirect_uri = "http://localhost:8888/callback/"
        client_id = self.client_id
        state = GenerateStr.GenStr(16)
        token_url = "https://accounts.spotify.com/authorize?"
        scope = 'user-read-private user-top-read'

        data = urlparse.urlencode({"response_type": "code", "client_id": client_id, "scope": scope, "redirect_uri": redirect_uri, "state": state})

        request_url = token_url + data

        r = requests.get(request_url)
        r1 = requests.get(r.url)

        print(r.url)
        #webbrowser.open(f"{r.url}")
        print("\n")
        refresh_link = input("Please login and paste the URL here: ")
        print("\n")
        dic = urlparse.parse_qs(refresh_link)
        self.refresh_link = dic["/callback/?code"]
        return self.refresh_link

    def get_access_token(self):
        
        redirect_uri = "http://localhost:8888/callback/"
        authorization_code = self.get_authorization_code()
        client_creds = f"{self.client_id}:{self.client_secret}"
        client_creds_64 = base64.b64encode(client_creds.encode())

        api_url = "https://accounts.spotify.com/api/token"

        data = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": redirect_uri
        }

        headers = {
            "Authorization": f"Basic {client_creds_64.decode()}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        r = requests.post(api_url, data=data, headers=headers)
        print(r.status_code)
        print("\n")
        print(r.json())
        print("\n")
        dic = r.json()
        return dic["access_token"]

    def get_users_top_items(self):
        
        access_token = self.get_access_token()
        type_q = "tracks" #could be tracks or artists
        request_link = "https://api.spotify.com/v1/me/top/{}".format(type_q)

        query = {
            "limit": 20, #The maximum number of itens to return. Min = 1, Max = 50.
            "offset": 0, #The index of the first item to return. Default: 0 (the first item). Use with limit to get the next set of items.
            "time_range": "short_term" #Over what time frame the affinities are computed. 
                                        #Valid values: long_term (calculated from several years of data and including all new data as it becomes available), 
                                        # medium_term (approximately last 6 months), short_term (approximately last 4 weeks). 
                                        # Default: medium_term 
        }

        header = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        r = requests.get(request_link, headers=header)
        print("\n")
        print(r.status_code)
        print("\n")
        for i in range(len(r.json()["items"])):
            print(r.json()["items"][i]["name"])
        print("\n")   
        return r.json()["items"]   


 
client = Spotify(client_id, client_secret)

# client.get_access_token()
# client.get_authorization_code()
client.get_users_top_items()


