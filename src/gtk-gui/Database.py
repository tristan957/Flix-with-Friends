import httplib2
import os
import xlwt
import xlrd
import tmdbsimple as tmdb

from xlutils.copy import copy
from Movie import Movie
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from itertools import count

try:
	import argparse
	flags = argparse.ArgumentParser(parents = [tools.argparser]).parse_args()
except ImportError:
	flags = None

# Flix with Friends special variables
# Creds stored at ~/.config/Flix-with-Friends/sheets.googleapis.flix-with-friends.json
# The google doc ID = 1OPg5wtyTFglYPGNYug4hDbHGGfo_yP9HOMRVjT29Lf8

# This scope gives read and write access
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Flix with Friends'
tmdb.API_KEY = 'b299f0e8dce095f8ebcbae6ab789005c'
LOCAL_EXCEL_FILE = 'local2.xlsx'
# LOCAL_EXCEL_FILE = 'testing.xlsx'


class Database:
	global location
	global docID
	_ids = count(0)

	def __init__(self, FN = None):
		self.fileName = ''
		self.dictionary = []  # cellular array of Excel file
		self.movies = []  # array of movies as class Movies
		self.fileName = FN
		self.listGenres = []
		self.MISSING_DATA = 'N/A' #need to update Movie.bad_movie if this is changed
		self.spreadsheetID = ''
		self.oldest_year = 3000
		self.friends = []
		self.troubled_list = [] # array of movies with bad data
		self.movieTitles = []
		self.id = next(self._ids)

		if FN is not None:
			self.loadDB()
			self.get_images()

	def loadDB(self):
		# Get data from Excel and load it into the Database object
		self.createDictionary()

		# Add Movies to movie list
		for movie in self.dictionary:
			m = Movie(movie)
			if m.bad_movie() or m.title in self.movieTitles:
				self.troubled_list.append(m)
			else:
				self.addMovie(m)

		self.movies.sort(key = lambda x: x.title)
		self.listGenres = sorted(self.listGenres)
		self.friends = sorted(self.friends)

		if len(self.troubled_list) and self.id == 1:
			print('Troubled Movies:')
			for m in self.troubled_list:
				print(m.title)

	def createDictionary(self):
		# This method converts all the data in the excelDB into a list of dictionaries
		# Access data by self.dictionary[row]['columnName']
		workbook = xlrd.open_workbook(self.fileName, on_demand=True)
		worksheet = workbook.sheet_by_index(0)
		first_row = []  # The row where we stock the name of the column
		for col in range(worksheet.ncols):
			first_row.append(worksheet.cell_value(0, col))

		# transform the workbook to a list of dictionaries
		for row in range(1, worksheet.nrows):
			elm = {}
			for col in range(worksheet.ncols):
				elm[first_row[col]] = worksheet.cell_value(row, col)
			self.dictionary.append(elm)

	def updateMovieInfo(self, movie, row):
		# This method updates all columns of a single movie in the DB
		rb = xlrd.open_workbook(self.fileName)  # Open the excel file
		wb = copy(rb)  # make a writeable copy of the open excel file
		w_sheet = wb.get_sheet(0)  # read the frist sheet to write to

		results = self.tmdb_search(movie,1)
		if not results:
			print(movie, self.MISSING_DATA)  # Print to console
			w_sheet.write(row, 2, '1') #runtime
			w_sheet.write(row, 3, self.MISSING_DATA) # genres
			w_sheet.write(row, 4, self.MISSING_DATA) # release date
			w_sheet.write(row, 5, '1') # vote count
			w_sheet.write(row, 6, self.MISSING_DATA) # overview
			w_sheet.write(row, 7, '1') # TMDB ID number
			w_sheet.write(row, 8, self.MISSING_DATA) # poster path
			w_sheet.write(row, 9, self.MISSING_DATA) # ActorsName
			w_sheet.write(row, 10, self.MISSING_DATA) # ActorsImg
			w_sheet.write(row, 11, self.MISSING_DATA) # ActorsChar
			w_sheet.write(row, 12, self.MISSING_DATA) # DirectorsName
			w_sheet.write(row, 13, self.MISSING_DATA) # DirectorsImg
			w_sheet.write(row, 14, self.MISSING_DATA) # Trailer
			w_sheet.write(row, 15, self.MISSING_DATA) # Backdrop
			w_sheet.write(row, 16, self.MISSING_DATA) # Keywords
		else:
			movie = results[0]
			w_sheet.write(row, 0, movie.title)
			w_sheet.write(row, 2, movie.runtime)
			w_sheet.write(row, 3, movie.get_genres_string())
			w_sheet.write(row, 4, movie.release_date)
			w_sheet.write(row, 5, movie.vote)
			w_sheet.write(row, 6, movie.overview)
			w_sheet.write(row, 7, movie.ID)
			w_sheet.write(row, 8, movie.poster_path)
			w_sheet.write(row, 9, self.stringify(movie.actorNames)) # ActorsName
			w_sheet.write(row, 10, self.stringify(movie.actorImg)) # ActorsImg
			w_sheet.write(row, 11, self.stringify(movie.actorChars)) # ActorsChar
			w_sheet.write(row, 12, movie.directorName) # DirectorsName
			w_sheet.write(row, 13, movie.directorImg) # DirectorsImg
			w_sheet.write(row, 14, movie.trailer) # Trailer
			w_sheet.write(row, 15, movie.backdrop) # Backdrop
			w_sheet.write(row, 16, self.stringify(movie.keywords)) # Keywords
			movie.get_image()

		wb.save(self.fileName)  # Save DB edits

	def update(self):
		# Updates all movies' data in DB
		p = len(self.dictionary)
		for i, Movie in enumerate(self.dictionary):
			self.updateMovieInfo(Movie['Title'], i + 1)
			# Display Percentage to console
			print('Percentage Complete: {0:.0f} %'.format(i / p * 100))
		print('Percentage Complete: 100 %')
		print('Database Update Complete')

	def addMovie(self, MOVIE):
		# Add Movie to List of Movies

		# Check if Movie has a new genre
		for g in MOVIE.genres:
			if g not in self.listGenres:
				if g != '' and g != self.MISSING_DATA:
					self.listGenres.append(g)

		# Check if Movie has a new Oldest release year
		if MOVIE.release_date[:4] < str(self.oldest_year):
			self.oldest_year = int(MOVIE.release_date[:4])

		# Add Friend if Movie has a friend not accounted for
		for v in MOVIE.viewers:
			if v not in self.friends:
				if v != '':
					self.friends.append(v)

		self.movies.append(MOVIE)
		self.movieTitles.append(MOVIE.title)

	def newMovie(self, movie_title):
		# Add a new movie just with a movie title
		self.updateMovieInfo(movie_title, len(self.movies) + 1)
		self.loadDB()

	def find_movie(self, title):
		for movie in self.movies:
			if movie.title == title:
				return movie

	def stringify(self, array):
		string = ''
		for i, item in enumerate(array):
			string = string + str(item)
			if i < len(array) - 1:
				string = string + ', '
		return string

	def get_images(self):
		for m in self.movies:
			m.get_image()

	def tmdb_search(self, keyword, num=5):
		# This function is used to run a keyword and return the results as
		# a list of movies

		search = tmdb.Search() # Setup search to run API query
		response = search.movie(query = keyword)  # Search for movie
		results = []
		count = 0
		for s in search.results:
			titleID = s['id']
			movieTMDB = tmdb.Movies(titleID)
			response = movieTMDB.info()
			videoResponse = movieTMDB.videos() # Trailers
			creditsResponse = movieTMDB.credits() # Cast/Crew
			keywordResponse = movieTMDB.keywords()
			# Can add critic reviews and similar movies as well

			# Keywords
			keywords = []
			for key in keywordResponse['keywords']:
				keywords.append(key['name'])

			# Trailer URL
			trailer = ''
			if len(videoResponse['results']):
				trailer = 'https://www.youtube.com/watch?v=' + videoResponse['results'][0]['key']

			# Top 3 Actors
			actorsName = []
			actorsChar = []
			actorsImg = []
			for key in creditsResponse['cast'][:3]:
				actorsName.append(str(key['name']))
				actorsChar.append(str(key['character']))
				actorsImg.append(str(key['profile_path']))

			# Director
			directorName = ''
			directorImg = ''
			for key in creditsResponse['crew']:
				if key['job'] == 'Director':
					directorName = key['name']
					directorImg = key['profile_path']

			# Get Genres into one line
			genreResult = response['genres']
			gen = ''
			for i in range(0, len(genreResult)):
				gen = gen + str(genreResult[i]['name'])
				if i < len(genreResult):
					gen = gen + ', '

			dictionary = {
				'Title': response['title'],
				'ID': titleID,
				'Runtime': response['runtime'],
				'Genres': gen,
				'ReleaseDate': response['release_date'],
				'Vote': response['vote_average'],
				'Overview': response['overview'],
				'ViewedBy': '',
				'Poster': response['poster_path'],
				# new to add below
				'Backdrop': response['backdrop_path'],
				'Trailer': trailer,
				'ActorsName': self.stringify(actorsName),
				'ActorsChar': self.stringify(actorsChar),
				'ActorsImg': self.stringify(actorsImg),
				'DirectorName': directorName,
				'DirectorImg': directorImg,
				'Keywords': self.stringify(keywords)
				}
			results.append(Movie(dictionary))
			count = count + 1
			if count == num:
				return results

	# The following are functions accesing and pushing from a Google Sheet
	def get_credentials(self):
		# Gets valid user credentials from storage.
		# If nothing has been stored, or if the stored credentials are invalid,
		# the OAuth2 flow is completed to obtain the new credentials.
		# Returns: Credentials, the obtained credential.

		home_dir = os.path.expanduser('~')
		credential_dir = os.path.join(home_dir, '.config/Flix-with-Friends')
		if not os.path.exists(credential_dir):
			os.makedirs(credential_dir)
		credential_path = os.path.join(credential_dir,
										'sheets.googleapis.flix-with-friends.json')

		store = Storage(credential_path)
		credentials = store.get()
		if not credentials or credentials.invalid:
			flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
			flow.user_agent = APPLICATION_NAME
			if flags:
				credentials = tools.run_flow(flow, store, flags)
			else: # Needed only for compatibility with Python 2.6
				credentials = tools.run(flow, store)
			print('Storing credentials to ' + credential_path)
		return credentials

	def get_google_doc(self, sheetID):
		# Run Google OAuth2
		credentials = self.get_credentials()
		http = credentials.authorize(httplib2.Http())
		discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
						'version=v4')
		service = discovery.build('sheets', 'v4', http = http,
									discoveryServiceUrl = discoveryUrl)

		# Pull data from the Google Sheet
		docID = self.spreadsheetID = sheetID
		rangeName = 'Sheet1!A:Q'
		result = service.spreadsheets().values().get(
			spreadsheetId = self.spreadsheetID, range = rangeName).execute()
		values = result.get('values', [])

		# Add values to the Excel sheet
		book = xlwt.Workbook(encoding = "utf-8")
		sheet1 = book.add_sheet("Sheet 1")
		updateNum = len(values)

		if not values:
			print('No data found.')
		else:
			i = 0
			for row in values:
				if row[0] == 'UpdateBelow':
					updateNum = i
				else:
					sheet1.write(i, 0, row[0])
					if len(row) > 8:
						for j in range(1,len(row)):
							sheet1.write(i, j, row[j])
					else:
						sheet1.write(i, 2, '0') #runtime
						sheet1.write(i, 3, self.MISSING_DATA) # genres
						sheet1.write(i, 4, self.MISSING_DATA) # release date
						sheet1.write(i, 5, '0') # vote count
						sheet1.write(i, 6, self.MISSING_DATA) # overview
						sheet1.write(i, 7, '0') # TMDB ID number
						sheet1.write(i, 8, self.MISSING_DATA) # poster path
						sheet1.write(i, 9, self.MISSING_DATA) # ActorsName
						sheet1.write(i, 10, self.MISSING_DATA) # ActorsImg
						sheet1.write(i, 11, self.MISSING_DATA) # ActorsChar
						sheet1.write(i, 12, self.MISSING_DATA) # DirectorsName
						sheet1.write(i, 13, self.MISSING_DATA) # DirectorsImg
						sheet1.write(i, 14, self.MISSING_DATA) # Trailer
						sheet1.write(i, 15, self.MISSING_DATA) # Backdrop
						sheet1.write(i, 16, self.MISSING_DATA) # Keywords
					i += 1

		book.save(LOCAL_EXCEL_FILE)
		self.fileName = Database.location = LOCAL_EXCEL_FILE

		# If UpdateBelow was Present, Update Movies Below that Point
		if updateNum != len(values):
			for i,row in enumerate(values[updateNum+1:]):
				self.updateMovieInfo(row[0], i + updateNum)
				# Check if there were viewers
				if len(row) > 1:
					rb = xlrd.open_workbook(self.fileName)  # Open the excel file
					wb = copy(rb)  # make a writeable copy of the open excel file
					w_sheet = wb.get_sheet(0)  # read the frist sheet to write to
					w_sheet.write(i + updateNum, 1, row[1]) #Viewers
					wb.save(self.fileName)  # Save DB edits


		# book.save(LOCAL_EXCEL_FILE)
		self.loadDB()

	def upload_google_doc(self):
		# Run Google OAuth2
		credentials = self.get_credentials()
		http = credentials.authorize(httplib2.Http())
		discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
						'version=v4')
		service = discovery.build('sheets', 'v4', http = http,
									discoveryServiceUrl = discoveryUrl)

		# Open the Excel sheet to read in data
		workbook = xlrd.open_workbook(self.fileName, on_demand = True)
		worksheet = workbook.sheet_by_index(0)

		# transform the workbook to a 2D list
		values = []
		for row in range(worksheet.nrows):
			elm = []
			for col in range(worksheet.ncols):
				elm.append(worksheet.cell_value(row, col))
			values.append(elm)

		# Make Sure Last Element is Blank
		values.append(16 * [''])

		# Upload values to the Google Sheet
		body = {
			'values': values
		}
		range_name = 'Sheet1!A1'
		result = service.spreadsheets().values().update(
			spreadsheetId=self.spreadsheetID, range=range_name,
			valueInputOption='USER_ENTERED', body=body).execute() # USER_ENTERED or RAW


if __name__ == "__main__":
	db = Database()
	doc_id = '1OPg5wtyTFglYPGNYug4hDbHGGfo_yP9HOMRVjT29Lf8'
	db.get_google_doc(doc_id)
	# db.update()
	db.upload_google_doc()
	# db.update()
