# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl
class Song(object):
	def__init__(self,artist,track):
		self.artist=artist      #we are creating these classes because later on when we have to access a song or an artist
		self.track=track        #its better to have it as an object
class Playlist(object):
	def__init__(self, id, title):
		self.id=id
		self.title=title
class YouTubeClient(object):        
#will contain methods that are going to interact with youtube API
    def__init__(self,credentials_location):      								#pass a credentials location parameter
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    	# Disable OAuthlib's HTTPS verification when running locally.
    	# *DO NOT* leave this option enabled in production.
    	os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    	api_service_name = "youtube"
    	api_version = "v3"
    	client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"
	
    	# Get credentials and create an API client
    	flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(credentials_location, scopes)     #here too
    	credentials = flow.run_console()
    	youtube = googleapiclient.discovery.build(
    	    api_service_name, api_version, credentials=credentials)				
    	self.youtube_client=youtube_client									#add this line
    																		#remove extra code

if __name__ == "__main__":
    main()
    def get_playlists(self):
    	request=self.youtube_client.playlists().list(
    		part="id, snippet",  #part variable need two parameters, id and snippet
    		maxresults=50,       #maxresults specify we can get maximum of 50 playlists
    		mine=True            #it specify that youtube just give your own playlist and not of someone else that we have saved
    		)
    	response = request.execute()   #execute the request and store in the respose variable
    	playlists=[Playlist(item['id'],item['snippet']['title']) for item in response['items']]  #now youtube gonna come back with a lot of data in this variable, but we care about
    	#only list of playlists, so we use this list compr. which go through respose dict and and get the key items
    	return playlists    #and return  as a list of playlists
    def get_videos_from_playlists(self,playlist_id):       #to get video list
    	request=self.youtube_client.playlistItems().list(
    		playlistId=playlist_id,
    		part= "id, snippet"
    		)
    	response=request.execute()
    	songs=[]
    	for item in request['items']:    #we need to get data from each video in response because youtube does not give us
    		video_id=item['snippet']['resourceId']['videoId']    #artists and track so need to get them ourselves
    		artist, track=get_artist_and_song_from_video(video_id)
    		if artist and track:        
    			songs.append(Song(artist,track))     #
    	return songs
    def get_artist_and_song_from_video(self,video_id):
    	youtube_url=f"http://youtube.com/watch?v={video_id}"
    	video= youtube_dl.YouTubeDL({'qutie': True}).extract_info(     #to get rid of output logs
    		youtube_url, download=False         #so that youtube_dl does not download he video
    		)
    	artist=video['artist']
    	track=video['track']
    	return artist, track



