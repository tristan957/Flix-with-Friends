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

try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags = None

# Flix with Friends special variables
# Creds stored at ~/.credentials/sheets.googleapis.flix-with-friends.json
# The google doc ID = 1OPg5wtyTFglYPGNYug4hDbHGGfo_yP9HOMRVjT29Lf8

# This scope gives read and write access
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Flix with Friends'
tmdb.API_KEY = 'b299f0e8dce095f8ebcbae6ab789005c'
LOCAL_EXCEL_FILE = 'local.xlsx'


class Database:
	global location
	global docID

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

		if FN is not None:
			self.loadDB()

	def loadDB(self):
		# Get data from Excel and load it into the Database object
		self.createDictionary()

		# Add Movies to movie list
		for movie in self.dictionary:
			m = Movie(movie)
			if m.bad_movie():
				self.troubled_list.append(m)
			else:
				self.addMovie(m)

		self.movies.sort(key = lambda x: x.title)
		self.listGenres = sorted(self.listGenres)
		self.friends = sorted(self.friends)
		# if len(self.troubled_list) > 0:
		# 	print('Troubled Movies:')
		# 	for m in self.troubled_list:
		# 		print(m.title)

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
		if len(results) == 0:
			print(movie, self.MISSING_DATA)  # Print to console
			w_sheet.write(row, 2, '0') #runtime
			w_sheet.write(row, 3, self.MISSING_DATA) # genres
			w_sheet.write(row, 4, self.MISSING_DATA) # release date
			w_sheet.write(row, 5, '0') # vote count
			w_sheet.write(row, 6, self.MISSING_DATA) # overview
			w_sheet.write(row, 7, '0') # TMDB ID number
			w_sheet.write(row, 8, self.MISSING_DATA) # poster path
		else:
			movie = results[0]
			w_sheet.write(row, 0, movie.title)
			w_sheet.write(row, 2, movie.runtime)
			w_sheet.write(row, 3, movie.genres_string())
			w_sheet.write(row, 4, movie.release_date)
			w_sheet.write(row, 5, movie.vote)
			w_sheet.write(row, 6, movie.overview)
			w_sheet.write(row, 7, movie.ID)
			w_sheet.write(row, 8, movie.poster_path)
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
		for g in MOVIE.genres:
			if g not in self.listGenres:
				if g != '' and g != self.MISSING_DATA:
					(self.listGenres).append(g)

		if MOVIE.release_date[:4] < str(self.oldest_year):
			self.oldest_year = int(MOVIE.release_date[:4])

		for v in MOVIE.viewers:
			if v not in self.friends:
				if v != '':
					self.friends.append(v)

		self.movies.append(MOVIE)

	def newMovie(self, movie_title):
		# Add a new movie just with a movie title
		self.updateMovieInfo(movie_title, len(self.movies) + 1)
		self.loadDB()

	def find_movie(self, title):
		for movie in self.movies:
			if movie.title == title:
				return movie

	def tmdb_search(self, keyword, num=5):
		# This function is used to run a keyword and return the results as
		# a list of movies

		search = tmdb.Search() # Setup search to run API query
		response = search.movie(query = keyword)  # Search for movie
		results = []
		i = 0
		for s in search.results:
			titleID = s['id']
			daMovie = tmdb.Movies(titleID)
			response = daMovie.info()
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
				'Poster': response['poster_path']
				}
			results.append(Movie(dictionary))
			i += 1
			if i == num:
				break
		return results

	# The following are functions accesing and pushing from a Google Sheet
	def get_credentials(self):
		# Gets valid user credentials from storage.
		# If nothing has been stored, or if the stored credentials are invalid,
		# the OAuth2 flow is completed to obtain the new credentials.
		# Returns: Credentials, the obtained credential.

		home_dir = os.path.expanduser('~')
		credential_dir = os.path.join(home_dir, '.credentials')
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
		rangeName = 'Sheet1!A:I'
		result = service.spreadsheets().values().get(
			spreadsheetId = self.spreadsheetID, range = rangeName).execute()
		values = result.get('values', [])

		# Add values to the Excel sheet
		book = xlwt.Workbook(encoding = "utf-8")
		sheet1 = book.add_sheet("Sheet 1")
		if not values:
			print('No data found.')
		else:
			i = 0
			for row in values:
				sheet1.write(i, 0, row[0])
				sheet1.write(i, 1, row[1])
				sheet1.write(i, 2, row[2])
				sheet1.write(i, 3, row[3])
				sheet1.write(i, 4, row[4])
				sheet1.write(i, 5, row[5])
				sheet1.write(i, 6, row[6])
				sheet1.write(i, 7, row[7])
				sheet1.write(i, 8, row[8])
				i += 1

		book.save(LOCAL_EXCEL_FILE)
		self.fileName = Database.location = LOCAL_EXCEL_FILE
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
	rb = xlrd.open_workbook(db.fileName)  # Open the excel file
	wb = copy(rb)  # make a writeable copy of the open excel file
	w_sheet = wb.get_sheet(0)  # read the frist sheet to write to

	wb.save(db.fileName)  # Save DB edits

	db.upload_google_doc()
