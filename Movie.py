import os
import sys
import tmdbsimple as tmdb
import urllib.request


class Movie:

	def __init__(self, dictionary):
		self.title = dictionary['Title']
		self.ID = dictionary['ID']
		self.viewers = dictionary['ViewedBy'].split(', ')
		self.runtime = dictionary['Runtime']
		self.genres = dictionary['Genres'].split(', ')
		self.release_date = dictionary['ReleaseDate']
		self.vote = str(dictionary['Vote'])
		self.overview = dictionary['Overview']
		self.poster_path = dictionary['Poster']
		self.actorNames = dictionary['ActorsName'].split(', ')
		self.actorChars = dictionary['ActorsChar'].split(', ')
		self.actorImg = dictionary['ActorsImg'].split(', ')
		self.directorName = dictionary['DirectorName']
		self.directorImg = dictionary['DirectorImg']
		self.trailer = dictionary['Trailer']
		self.backdrop = dictionary['Backdrop']
		self.keywords = dictionary['Keywords'].split(', ')
		self.poster = "./images/movies/" + self.title.replace(" ", "") + '/' + self.title.replace(" ", "") + "_"

	def get_image(self):

		baseURL = 'https://image.tmdb.org/t/p/'
		updated = False # Used to check if a download was needed
		# Poster
		if (str(self.poster_path) != 'N/A') and str(self.poster_path) != 'None' and str(self.poster_path) != '':
			# Create imagePosters directory if not present
			os.makedirs("./images", exist_ok = True)
			os.makedirs("./images/movies", exist_ok = True)
			os.makedirs(self.poster, exist_ok = True)
			# posters = ['w92', 'w154', 'w185', 'w300_and_h450_bestv2', 'w342', 'w500', 'w780'] #'original']
			posters = ['w92', 'w342', 'w500']

			for p in posters:
				imagePage = baseURL + p + self.poster_path
				filename = self.title.replace(" ", "") + '_' + p + '.jpg'
				fullfilename = os.path.join('./images/movies/' + self.title.replace(" ", ""), filename)

				# if not already existent, download
				if not(os.path.isfile(fullfilename)):
					if not updated:
						print(self.title)
						updated = True
					urllib.request.urlretrieve(imagePage, fullfilename)
					print(p, 'poster image:', imagePage)

		# Actors images
		os.makedirs("./images/people", exist_ok = True)
		for i, actor in enumerate(self.actorImg):
			if actor != 'None' and actor != '':
				actorName = self.actorNames[i]

				imagePage = baseURL + 'w92' + actor
				filename = actorName.replace(" ", "") + '_' + 'w92.jpg'
				fullfilename = os.path.join('./images/people/', filename)

				# if not already existent, download
				if not(os.path.isfile(fullfilename)):
					if not updated:
						print(self.title)
						updated = True
					urllib.request.urlretrieve(imagePage, fullfilename)
					print(actorName, 'image:', imagePage)

		# Director Image
		if str(self.directorImg) != 'None' and str(self.directorImg) != '':
			imagePage = baseURL + 'w92' + self.directorImg
			filename = self.directorName.replace(" ", "") + '_' + 'w92.jpg'
			fullfilename = os.path.join('./images/people/', filename)

			# if not already existent, download
			if not(os.path.isfile(fullfilename)):
				if not updated:
					print(self.title)
					updated = True
				urllib.request.urlretrieve(imagePage, fullfilename)
				print(self.directorName, 'image:', imagePage)

	def get_markup_title(self):
		return "<big><b>" + self.title.replace('&', '&amp;') + "</b></big>"

	def get_markup_overview(self):
		return self.overview.replace('&', '&amp;')

	def get_genres_string(self):
		return ', '.join(self.genres).rstrip(', ')

	def get_viewers_string(self):
		return self.stringify(self.viewers)

	def stringify(self, array):
		string = ''
		for i, item in enumerate(array):
			string = string + str(item)
			if i < len(array) - 1:
				string = string + ', '
		return string

	def bad_movie(self):
		bad_title = (self.title == 'N/A')# or (len(self.title) == 0)
		bad_ID = (self.ID == '1')# or len(self.ID) == 0)
		bad_runtime = (self.runtime == '1')# or (len(self.runtime) == 0)
		bad_overview = (self.overview == 'N/A')# or (len(self.overview) == 0)
		bad_poster = self.poster_path == 'N/A'

		return bad_ID or bad_overview or bad_runtime or bad_title or bad_poster

	def get_small_image(self):
		# Returns w92 image
		filename = self.title.replace(" ", "") + '_w92.jpg'
		return os.path.join('./images/movies/' + self.title.replace(" ", ""), filename)

	def get_large_image(self):
		# Returns w342 image
		filename = self.title.replace(" ", "") + '_w342.jpg'
		return os.path.join('./images/movies/' + self.title.replace(" ", ""), filename)
