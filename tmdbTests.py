import tmdbsimple as tmdb





if __name__ == "__main__":
	tmdb.API_KEY = 'b299f0e8dce095f8ebcbae6ab789005c'
	youtubeURL = 'https://www.youtube.com/watch?v='
	imgPath = 'https://image.tmdb.org/t/p/w780'
	id = 263115
	movie = tmdb.Movies(id)
	genMovie = tmdb.Movies()

	# Movie INFO KEYS: runtime, revenue, title, adult, tagline, budget, production_countries, poster_path, vote_count, production_companies, genres, belongs_to_collection, imdb_id, video, popularity, vote_average, homepage, original_language, original_title, backdrop_path, spoken_languages, id, overview, release_date, status
	response0 = movie.info()
	# for key in response0:
	# 	print(key)
	print('Movie: ' + response0['title'])
	print('')

	# Trailer KEYS: results
	response = movie.videos()
	print(response['results'][0]['site'] + ' Trailer: ' + youtubeURL + response['results'][0]['key'])
	print('')

	# Credits KEYS: cast, id, crew
	response1 = movie.credits()

	# Get top 5 Actors
	print('Top 5 Actors and Director:')
	# Director
	for key in response1['crew']:
		if key['job'] == 'Director':
			print(key['name'] + ' -- ' + key['job'] + ' -- ' + imgPath + key['profile_path'])

	for key in response1['cast'][:5]:
		print(str(key['name']) + ' -- ' + str(key['character']) + ' -- ' + imgPath + str(key['profile_path']))
	print('')

	# Images KEYS: backdrops, posters, id
	response2 = movie.images()
	# for key in response2['posters']:
	# 	if key['iso_639_1'] == 'en':
	# 		print(str(key['width']) + ' x ' + str(key['height']) + ' -- '  'imgPath' + key['file_path'])
	print('Backdrops:')
	for key in response2['backdrops']:
		print(str(key['width']) + ' x ' + str(key['height']) + ' -- ' + imgPath + key['file_path'])
	# print(response2)
	print('')

	# Movie Reviews
	response3 = movie.reviews()
	# print(response3)

	# Similiar Movies
	response4 = movie.similar_movies()
	print('Similiar Movies:')
	for key in response4['results'][:5]:
		print(key['title'])
	print('')

	# Movies People Are Currently Watching
	response5 = genMovie.now_playing()
	print('Movies People Currently Watching:')
	for key in response5['results']:
		print(key['title'])
