import os
import sys
import tmdbsimple as tmdb
import urllib.request


class Movie:

	def __init__(self, dictionary):
		if '_id' in dictionary: self.db_id = dictionary['_id']

		self.title = ''
		self.ID = ''
		self.viewers = ''
		self.runtime = ''
		self.genres = []
		self.release_date = ''
		self.vote = ''
		self.overview = ''
		self.poster_path = ''
		self.actorNames = []
		self.actorChars = []
		self.actorImg = []
		self.directorName = ''
		self.directorImg = ''
		self.trailer = ''
		self.backdrop = ''
		self.keywords = ''

		if 'title' in dictionary:  self.title = dictionary['title']
		if 'id' in dictionary:  self.ID = dictionary['id']
		if 'viewers' in dictionary:  self.viewers = dictionary['viewers'].split(', ')
		if 'runtime' in dictionary:  self.runtime = dictionary['runtime']
		if 'genres' in dictionary:  self.genres = dictionary['genres']
		if 'release_date' in dictionary:  self.release_date = dictionary['release_date']
		if 'vote_average' in dictionary:  self.vote = str(dictionary['vote_average'])
		if 'overview' in dictionary:  self.overview = dictionary['overview']
		if 'poster_path' in dictionary:  self.poster_path = dictionary['poster_path']
		if 'actor_name' in dictionary:  self.actorNames = dictionary['actor_name']
		if 'actor_char' in dictionary:  self.actorChars = dictionary['actor_char']
		if 'actor_img' in dictionary:  self.actorImg = dictionary['actor_img']
		if 'director_name' in dictionary:  self.directorName = dictionary['director_name']
		if 'director_img' in dictionary:  self.directorImg = dictionary['director_img']
		if 'trailer' in dictionary:  self.trailer = dictionary['trailer']
		if 'backdrop_path' in dictionary:  self.backdrop = dictionary['backdrop_path']
		if 'keywords' in dictionary:  self.keywords = dictionary['keywords']
		self.poster = "./images/movies/" + self.title.replace(" ", "") + '/' + self.title.replace(" ", "") + "_"

		self.allActors = []
		self.director = Person('Director', self.directorName, self.directorImg)

		for i, actor in enumerate(self.actorNames):
			self.allActors.append(Person('actor', self.actorNames[i], self.actorImg[i], self.actorChars[i]))

	def get_image(self):

		baseURL = 'https://image.tmdb.org/t/p/'
		updated = False # Used to check if a download was needed
		# Poster
		if (str(self.poster_path) != 'N/A') and str(self.poster_path) != 'None' and str(self.poster_path) != '':
			# Create imagePosters directory if not present
			os.makedirs("./images", exist_ok = True)
			os.makedirs("./images/movies", exist_ok = True)
			os.makedirs('./images/movies/' + self.title.replace(" ", ""), exist_ok = True)
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
		for p in self.allActors:
			p.get_image()

		self.director.get_image()

	def get_markup_overview(self):
		return self.overview.replace('&', '&amp;')

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

class Person:

	def __init__(self, roleA, name, imgLink = '', charName = ""):
		self.role = roleA
		self.name = name
		self.imgLink = imgLink
		self.charName = charName
		self.img = ''

	def get_image(self):
		os.makedirs("./images/people", exist_ok = True)
		baseURL = 'https://image.tmdb.org/t/p/'

		if self.need_image():
			imagePage = baseURL + 'w92' + self.imgLink
			filename = self.name.replace(" ", "") + '_' + 'w92.jpg'
			self.img = './images/people/' + filename
			fullfilename = os.path.join('./images/people/', filename)

			# if not already existent, download
			if not(os.path.isfile(fullfilename)):
				urllib.request.urlretrieve(imagePage, fullfilename)
				print(self.name, 'image:', imagePage)

		if os.path.exists(self.img):
			return self.img
		return None

	def need_image(self):
		return self.imgLink is not None and self.imgLink != 'None' and self.imgLink != '' and not(os.path.exists(self.img))
