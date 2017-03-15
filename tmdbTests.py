import tmdbsimple as tmdb





if __name__ == "__main__":
	tmdb.API_KEY = 'b299f0e8dce095f8ebcbae6ab789005c'
	youtubeURL = 'https://www.youtube.com/watch?v='
	id = 857
	movie = tmdb.Movies(id)
	response = movie.videos()
	print(response['results'][0]['site'] + ': ' + youtubeURL + response['results'][0]['key'])
