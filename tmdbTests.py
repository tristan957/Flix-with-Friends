import tmdbsimple as tmdb





if __name__ == "__main__":
	tmdb.API_KEY = 'b299f0e8dce095f8ebcbae6ab789005c'
	youtubeURL = 'https://www.youtube.com/watch?v='
	imgPath = 'https://image.tmdb.org/t/p/w780'
	id = 857
	movie = tmdb.Movies(id)

	# Trailer KEYS: results
	response = movie.videos()
	# for key in response:
	# 	print(key)
	print(response['results'][0]['site'] + ': ' + youtubeURL + response['results'][0]['key'])
	print('')
	# Credits KEYS: cast, id, crew
	response1 = movie.credits()
	# for key in response1:
	# 	print(key)
	# print(response1)

	# Get top 5 Actors
	print('Top 5 Actors:')
	for key in response1['cast'][:5]:
		print(str(key['name']) + ' -- ' + str(key['character']) + ' -- ' + imgPath + str(key['profile_path']))
	print('')

	for key in response1['crew']:
		if key['job'] == 'Director':
			print(key['name'] + ' -- ' + key['job'] + ' -- ' + imgPath + key['profile_path'])
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
