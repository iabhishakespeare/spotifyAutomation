import json
import os  

import google_auth_oauthlib.flow
import googleapiclient.discovery  # youtube APIv3
import googleapiclient.errors

import requests
import youtube_dl

# takes the variable we want from secret file
from secret import spotify_user_id, spotify_token


class CreatePlaylist:

    def __init__(self):  
        self.user_id = spotify_user_id  # takes the username in our secret file
        self.spotify_token = spotify_token
        self.youtube_client = self.get_youtube_client()
        self.all_song_info = {}

    # STEP 1: Sign into youtube  
    def get_youtube_client(self):
        # COPIED FROM YOUTUE DATA API
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"  # this is MY special id number

        # Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()

        # From YOUTUBE_API
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube_client

    # STEP 2: grab like song on youtube // and create a dictionary of important song info
    def get_liked_videos(self):  
        request = self.youtube_client.videos().list(
            part="snippet,contentDetails,statistics",
            myRating="like"
        )
        response = request.execute()

        # collect each video and get important info #loops through all song called item
        for item in response["items"]:
            video_title = item["snipped"]["title"]
            # plug in URL HERE (not done)
            youtube_url = "https://www.youtube.com/watch?v={}".format(
                item["id"])

            # use youtube_dl lib to collect the song name and artist
            video = youtube_dl.YoutubeDL({}).extract_info(
                youtube_url, download=False)

            song_name = video["track"]
            artist = video["artist"]

            # save imported information
            self.all_song_info[video_title] = {
                "youtube_url": youtube_url,
                "song_name": song_name,
                "artist": artist,

                # add the uri, easy to get song to put into Playlist
                # call the function we wrote
                "spotify_uri": self.get_spotify_uri(song_name, artist)
            }