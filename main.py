import json
import requests
from secrets import spotify_user_id, discover_weekly_id
from datetime import date
from refresh import Refresh


class SaveSongs:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = ""
        self.discover_weekly_id = discover_weekly_id
        self.tracks = ""
        self.new_playlist_id = ""

    def find_songs(self):
        print("Finding songs in discover weekly...")
        #loop through playlist tracks and add them to list
        query = f"https://api.spotify.com/v1/playlists/{discover_weekly_id}/tracks"

        response = requests.get(query, headers={"Content-Type": "application/json","Authorization": f"Bearer {self.spotify_token}"})
        response_json = response.json()

        for i in response_json["items"]:
            self.tracks += (i["track"]["uri"] + ",")
        self.tracks = self.tracks[:-1]  # remove last comma

        self.add_to_playlist()


    def create_playlist(self):
        print("Creating Playlist...")
        today = date.today()
        today_formatted = today.strftime("%d/%m/%y")

        query = f"https://api.spotify.com/v1/users/{spotify_user_id}/playlists"

        request_body = json.dumps({
            "name": "Discover weekly " + today_formatted, "description": "Saved discover weekly playlist", "public": True
        })

        response = requests.post(query, data=request_body, headers={"Content-Type": "application/json","Authorization": f"Bearer {self.spotify_token}"})
        response_json = response.json()
        return response_json["id"]


    def add_to_playlist(self):

        self.new_playlist_id = self.create_playlist()
        print("new pl id " + self.new_playlist_id)

        print("Adding songs...")
        query = f"https://api.spotify.com/v1/playlists/{self.new_playlist_id}/tracks?uris={self.tracks}"
        response = requests.post(query, headers={"Content-Type": "application/json","Authorization": f"Bearer {self.spotify_token}"})

        print("Done")


    def call_refresh(self):
        print("Refreshing token")
        refresh_caller = Refresh()
        self.spotify_token = refresh_caller.refresh()
        print(self.spotify_token)

        self.find_songs()


a = SaveSongs()
a.call_refresh()