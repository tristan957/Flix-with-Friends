
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
