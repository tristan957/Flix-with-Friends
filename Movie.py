import os
import sys
import tmdbsimple as tmdb
import urllib.request


class Movie:

	def __init__(self, tI='', rU=0, gE=[], rD='', vO=0, oV='', vI=[]):
		self.title = tI
		self.runtime = rU
		self.genres = gE
		self.release_date = rD
		self.vote = vO
		self.overview = oV
		self.viewers = vI

	def __init__(self, dictionary):
		self.title = dictionary['Title']
		self.ID = dictionary['ID']
		self.viewers = dictionary['ViewedBy'].split(', ')
		self.runtime = dictionary['Runtime']
		self.genres = dictionary['Genres'].split(', ')
		self.release_date = dictionary['ReleaseDate']
		self.vote = dictionary['Vote']
		self.overview = dictionary['Overview']
		self.poster_path = dictionary['Poster']

	def get_image(self):
		if (self.poster_path != 'N/A'):
			# Create imagePosters directory if not present
			os.makedirs("./imagePosters", exist_ok=True)
			baseURL = 'https://image.tmdb.org/t/p/'
			posters = ['w92', 'w154', 'w185', 'w300_and_h450_bestv2', 'w342', 'w500', 'w780'] #'original']

			for p in posters:
				imagePage = baseURL + p + self.poster_path
				print(p, 'poster image:', imagePage)
				filename = self.title.replace(" ", "") + '_' + p + '.jpg'
				fullfilename = os.path.join('./imagePosters', filename)

				# if not already existent, download
				if not(os.path.isfile(fullfilename)):
					# COMMENT ME OUT TO NOT DOWNLOAD EVERYTHING
					urllib.request.urlretrieve(imagePage, fullfilename)
			print('')
