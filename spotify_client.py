import requests
import urllib.parse
class SpotifyClient(object):
	def __init__(self):
		pass
	def search_songs(self, artist, track):
		query= urllib.parse.quote(f'{artist}{track}')                      #to search a song you need to formulate a geturl string
		url=f"https://api.spotify.com/v1/search?q={query}&type=track"    #to specify that we are searching for a track
		respose=request.get(     #to issue the request to spotify web API(we use get request)
		url,
		headers={
			"Content-Type": "application/json",   #this header will specify to spotify api that we are expecting a response that contains json
			"Authorization": f"Bearer{self.api_token}"   #here we will pass the oauth token
			}
		)
		response_json=response.json()    #this will help to get the response as a json object

		result= response_json['tracks']['items']     #we will get list of  results from the response we get from api
		if results:
			#lets assume the first song is the list if the song we want
			return results[0]['id']  #we will return the id of first result from the list
		else:
			raise Exception(f"no song found for {artist}={track}") 

	def add_songs_to_spotify(self, song_id):
		url=f"https://api.spotify.com/v1/me/tracks"
		response=request.put(       #here we will issue a put request
			url,
			json={           #it will have keys ids that will have a list/array of all the song ids that we wanna add to our liked songs
			"ids": [song_id]
			},
			headers={
			"Content-Type": "application/json",   #this header will specify to spotify api that we are expecting a response that contains json
			"Authorization": f"Bearer{self.api_token}"   #here we will pass the oauth token
			}
		)
		return response.ok   #it will return true or false
	