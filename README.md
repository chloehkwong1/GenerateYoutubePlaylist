# GenerateYoutubePlaylist
Want to lyric videos for your favourite Spotify playlist so you can sing along? Or prehaps you want to see what the music videos look like! This programme creates Youtube playlists from Spotify playlists given an identifer (playlist ID, URL or URI).

## Getting Started
### Technologies Used
- [YouTube Data API v3](https://developers.google.com/youtube/v3)
- [Spotify API](https://developer.spotify.com/documentation/web-api/)
- [Spotipy](https://spotipy.readthedocs.io/en/2.13.0/) - a lightweight Python library for Spotify API

### Prerequisites
- Python 2.6 or greater
- The pip package management tool
- A Google account
- A Spotify account

### Local Setups
Install all dependencies: 
```
pip install -r requirements.txt
```
### Youtube Setups
1. Create a new project in the Google [API Console](https://console.developers.google.com/apis/dashboard).

2. Check that [Youtube Data API v3](https://console.developers.google.com/apis/library/youtube.googleapis.com) is enabled for your new project.

3. Within Youtube Data API, open up the [Credentials Panel](https://console.developers.google.com/apis/credentials). Create two credentials:
- **API key**
- **OAuth 2.0 client ID** - for Application Type select "Desktop App". Before being able to make this you might be required to go through an OAuth consent screen. All you have to do is give it a name and then press save. 

For more information, read Step 1 of the [Youtube API Python Quickstart](https://developers.google.com/youtube/v3/quickstart/python) page.

4. Download the OAuth 2.0 Client ID JSON file and copy and paste the contents into the youtube_secrets.json file (Or rename your file to youtube_secrets.json and use that instead).

### Spotify Setups
1. Go to the [Spotify Developers Dashboard](https://developer.spotify.com/dashboard/applications) and create a new app. 
2. Copy and paste the Client ID and Client Secret into the spotify_secrets.py file under the variable names spotify_client_id and spotify_client_secret respectively. 


## Running the Spotify to Youtube app
1. The spotify_to_youtube.py file can now be run from an IDE or the command line.
2. When run, the first input should be the URL/URI/ID of the Spotify playlist you want to convert. From the desktop app, identifers can be found by clicking on the 3 dots icon (next to the playlist PLAY button) and then clicking on SHARE. On the [Spotify Web Player](https://open.spotify.com/) the URL can just copied straight from the address bar.
3. There should then be a series of authorisation steps asking you to paste a URL in your web browser and then another asking you to paste a code back into the command line. 
4. There is the option for the Youtube playlist to contain videos consisting of lyric videos or M/V's (if available).
```
"For lyric videos type 'L', else for music videos just press ENTER: "
```
5. After these steps are followed, the YouTube playlist should be available in the [Youtube Library](https://www.youtube.com/feed/library).

## Errors/ Troubleshooting
There are currently two main errors I have been facing when running this code, neither of which I know how to fix. Any help would be appreciated!
- ```HttpError: <HttpError 403 when requesting https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&order=relevance&q=SONGNAME&alt=json returned "The request cannot be completed because you have exceeded your <a href="/youtube/v3/getting-started#quota">quota</a>.">``` 
This one is  hitting the Google daily quota limit of 10000 requests, however it's happening after only one code run. Any ideas how I can either increase my quota or decrease the quota usage?  
- ```HttpError: <HttpError 500 when requesting https://www.googleapis.com/youtube/v3/playlists?part=snippet%2Cstatus&alt=json returned "Internal error encountered.">```
This error occurs on line:
``` response_create_playlist = request_create_playlist.execute() ```
Sometimes I get this error, sometimes I don't. Any ideas? Normally if this happens I just leave it a while and come back to it later. 

## Acknowledgments
* Thank you to [TheComeUpCode](https://github.com/TheComeUpCode/SpotifyGeneratePlaylist) for inspiration!
