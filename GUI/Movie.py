
class Movie:
	# Public variables - could be wrong, making class similiar to c++
	title = ''
	viewers = []
	runtime = 0
	genres = []
	release_date = ''
	vote = 0
	overview = ''

	def __init__(self):
		self.title = ''
		self.viewers = []
		self.runtime = 0
		self.genres = []
		self.release_date = ''
		self.vote = 0
		self.overview = ''

	def __init__(self, tI='', vI=[], rU=0, gE=[], rD='', vO=0, oV=''):
		self.title = tI
		self.viewers = vI
		self.runtime = rU
		self.genres = gE
		self.release_date = rD
		self.vote = vO
		self.overview = oV

	def __init__(self, dictionary):
		self.title = dictionary['Title']
		self.viewers = dictionary['ViewedBy']
		self.runtime = dictionary['Runtime']
		self.genres = dictionary['Genres'].split(', ')
		self.release_date = dictionary['ReleaseDate']
		self.vote = dictionary['Vote']
		self.overview = dictionary['Overview']
