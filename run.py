import os
from youtube_client import YouTubeClient
def run():
	#get a list of playlists from the youtube
	youtube_client= YoutubeClient('./creds/client_secret.json')    #to get all playlists from our youtube channel IMP: download credentials file in dir creds
	playlists= youtube_client.get_playlists()   #now we call the method that we created earliar and store it in playlists var
	#Ask which playlist we want to get music videos from
	for index, playlist in enumerate(playlists):    #we will enumerate the playlists and then we can choose from that list e.g. 0. Music 1.Old songs 3 Bhajans
		print(f"{index} : {playlist.title}")
	choice = int(input("Enter your Choice:"))
	chosen_playlist=playlists[choice]
	print(f"You selected: {chosen_playlist.title}")


	#for each video in the playlist, get the song info from youtube

	songs= youtube_client.get_videos_from_playlist(chosen_playlist.id)
	print(f"attempting to add (len(songs))")
	#Search for the song on Spotify
	for song in songs:
		spotify_song_id = spotify_client.search_song(song.artist, song.track)
		if spotify_song_id:
			added_song = spotify_client.add_song_to_spotify(spotify_song_id)
			if added_song:
				print(f"Added {song.artist}")
	
if __name__ == '__main__':
	main()