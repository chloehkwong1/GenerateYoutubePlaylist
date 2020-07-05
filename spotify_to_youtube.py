import json
import spotipy
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from datetime import date
from spotipy.oauth2 import SpotifyClientCredentials

from spotify_secrets import spotify_client_secret, spotify_client_id


class Create_Playlist:
    
    def __init__(self):
        self.results_loads = self.access_spotify()
        self.tracks_list = self.spotify_tracks_list()
        self.youtube = self.get_youtube_credentials()

    def access_spotify(self):
        client_credentials_manager = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        
        playlist_url = input("Please paste in the url of your Spotify playlist: ")
        results = sp.playlist(playlist_url)
        results_dumps = json.dumps(results, indent=4)
        results_loads = json.loads(results_dumps)
    
        return results_loads
    
    def spotify_tracks_list(self):
        
        tracks_list = []
        for song in self.results_loads["tracks"]["items"]:
            tracks_list.append("{artist} {song}".format(artist = song["track"]["artists"][0]["name"], song = song["track"]["name"]))
        
        return tracks_list
        
    
    def get_youtube_credentials(self):
        
        scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "youtube_secrets.json"
    
        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)
        
        return youtube
    
    def create_youtube_playlist(self):
        
        #Playlist to be lyrics videos or M/V's? 
        lyrics_or_mv = input("For lyric videos type 'L', else for music videos just press ENTER: ").upper()
        
        # Create the playlist
        request_create_playlist = self.youtube.playlists().insert(
            part="snippet,status",
            body={
              "snippet": {
                "title": "{playlist} {lyrics}".format(playlist = self.results_loads["name"], lyrics = "Lyrics" if lyrics_or_mv == 'L' else ''),
                "description": "This is your {} playlist from Spotify created on {}! Happy listening :)".format(self.results_loads["name"], date.today().strftime("%B %d, %Y")),
                "tags": [
                  "sample playlist",
                  "API call"
                ],
                "defaultLanguage": "en"
              },
              "status": {
                "privacyStatus": "private"
              }
            }
        )
        response_create_playlist = request_create_playlist.execute()
        
        #Search for each song and return a list of the videoId's for each Youtube video
        youtube_song_id_list = []        
        for track in self.tracks_list:
            request_search = self.youtube.search().list(
                part="snippet",
                maxResults=1,
                order="relevance",
                q= track + "{}".format("lyrics" if lyrics_or_mv == 'L' else '')
            )
            response_search = request_search.execute()
            youtube_song_id_list.append(response_search)
            
        song_id_dumps = json.dumps(youtube_song_id_list, indent=4)
        song_id_loads = json.loads(song_id_dumps)
        
        #Add the video for each Youtube Id to the playlist
        for item in song_id_loads:
            request_add_to_playlist = self.youtube.playlistItems().insert(
                part="snippet",
                body={
                  "snippet": {
                    #"playlistId": "{}".format(response_create_playlist["id"]),
                    'playlistId': response_create_playlist["id"],
                    "resourceId": {
                      "kind": "youtube#video",
                      #"videoId": "{}".format(item["items"][0]["id"]["videoId"])
                      "videoId": item["items"][0]["id"]["videoId"] 
                    }
                  }
                }
            )
            request_add_to_playlist.execute()  
            

if __name__ == "__main__":
    main = Create_Playlist()
