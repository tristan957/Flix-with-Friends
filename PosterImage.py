import sys
import tmdbsimple as tmdb
import urllib.request

def get_image(moviePoster):
	if moviePoster != '':
		url300_450 = 'https://image.tmdb.org/t/p/w300_and_h450_bestv2'
		imagePage = url300_450 + moviePoster
		print('URL image:',imagePage, '\n')
		# urllib.request.urlretrieve(imagePage, response['title'] + '.jpg')


if __name__ == "__main__":
	if len(sys.argv) > 1:
		arguments = sys.argv
		MOVIE = " ".join(arguments[1:])
		get_image(MOVIE)
