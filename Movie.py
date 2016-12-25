import sys
import tmdbsimple as tmdb
import urllib.request


def get_image(moviePoster):
	if moviePoster != '':
		url300_450 = 'https://image.tmdb.org/t/p/w300_and_h450_bestv2'
		imagePage = url300_450 + moviePoster
		print('URL image:',imagePage, '\n')
		# urllib.request.urlretrieve(imagePage, response['title'] + '.jpg')

class Movie:

	def __init__(self):
		self.title = ''
		self.ID = 0
		self.viewers = []
		self.runtime = 0
		self.genres = []
		self.release_date = ''
		self.vote = 0
		self.overview = ''
		self.poster_path = ''

	def __init__(self, tI='', vI=[], rU=0, gE=[], rD='', vO=0, oV=''):
		self.title = tI
		self.viewers = vI
		self.runtime = rU
		self.genres = gE
		self.release_date = rD
		self.vote = vO
		self.overview = oV

	# This might be the only init needed, depends on how the add movie dialog is going to be setup
	def __init__(self, dictionary):
		self.title = dictionary['Title']
		self.ID = dictionary['ID']
		self.viewers = dictionary['ViewedBy']
		self.runtime = dictionary['Runtime']
		self.genres = dictionary['Genres'].split(', ')
		self.release_date = dictionary['ReleaseDate']
		self.vote = dictionary['Vote']
		self.overview = dictionary['Overview']
		self.poster_path = dictionary['Poster']
