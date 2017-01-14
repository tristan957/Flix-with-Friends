import httplib2
import os
import xlwt
import xlrd
import tmdbsimple as tmdb

from xlutils.copy import copy
from Movie import Movie, get_image
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# Not really sure what this is, how Google documentation coded it
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


# Flix with Friends special variables
# Creds stored at ~/.credentials/sheets.googleapis.flix-with-friends.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Flix with Friends'
tmdb.API_KEY = 'b299f0e8dce095f8ebcbae6ab789005c'


class Database:
	global location

	def __init__(self):
		self.fileName = ''
		self.dictionary = []  # cellular array of Excel file
		self.movies = []  # array of movies as class Movies
		self.listGenres = []
		self.MISSING_DATA = 'N/A'
		self.spreadsheetID = ''

	def __init__(self, FN):
		self.fileName = ''
		self.dictionary = []  # cellular array of Excel file
		self.movies = []  # array of movies as class Movies
		self.fileName = FN
		self.listGenres = []
		self.MISSING_DATA = 'N/A'
		self.spreadsheetID = ''
		self.loadDB()

	def loadDB(self):
		self.createDictionary()

		# Add Movies to movie list
		for movie in self.dictionary:
			self.addMovie(Movie(movie))
		self.listGenres = sorted(self.listGenres)

	def createDictionary(self):
		# This method converts all the data in the excelDB into a Listed PY dictionary
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

	def updateMovieDB(self, movie, row):
		# This method updates all columns of a single movie in the DB
		rb = xlrd.open_workbook(self.fileName)  # Open the excel file
		wb = copy(rb)  # make a writeable copy of the open excel file
		w_sheet = wb.get_sheet(0)  # read the frist sheet to write to
		search = tmdb.Search() # Setup search to run API query
		response = search.movie(query = movie)  # Search for movie
		i = 0
		for s in search.results:  # for loop return first search result FIXME
			i = 1 + i
			if i == 1:
				titleID = s['id']
				daMovie = tmdb.Movies(titleID)
				response = daMovie.info()
				# Get Genres into one line
				genreResult = response['genres']
				gen = ''
				for i in range(0, len(genreResult)):
					gen += genreResult[i]['name']
					if i < (len(genreResult) - 1):
						gen += ', '
				# Write info to appropriate (row,column)
				w_sheet.write(row, 0, response['title'])
				w_sheet.write(row, 2, response['runtime'])
				if (gen is None) or (len(gen) == 0):
					w_sheet.write(row, 3, 'N/A')
				else:
					w_sheet.write(row, 3, gen)
				w_sheet.write(row, 4, response['release_date'])
				w_sheet.write(row, 5, response['vote_average'])
				w_sheet.write(row, 6, response['overview'])
				w_sheet.write(row, 7, titleID)

				if (response['poster_path'] is None) or (len(response['poster_path']) == 0):
					w_sheet.write(row, 8, 'N/A')
				else:
					w_sheet.write(row, 8, response['poster_path'])

		if i == 0:  # If no search results
			print(movie, self.MISSING_DATA)  # Print to console
			w_sheet.write(row, 2, self.MISSING_DATA) #runtime
			w_sheet.write(row, 3, self.MISSING_DATA) # genres
			w_sheet.write(row, 4, self.MISSING_DATA) # release date
			w_sheet.write(row, 5, '0') # vote count
			w_sheet.write(row, 6, self.MISSING_DATA) # overview
			w_sheet.write(row, 7, '0') # TMDB ID number
			w_sheet.write(row, 8, self.MISSING_DATA) # poster path

		wb.save(self.fileName)  # Save DB edits

	def update(self):
		# Updates all movies' data in DB
		p = len(self.dictionary)
		for i, Movie in enumerate(self.dictionary):
			self.updateMovieDB(Movie['Title'], i + 1)
			# Display Percentage to console
			print('Percentage Complete: {0:.0f} %'.format(i / p * 100))
		print('Percentage Complete: 100 %')
		print('Database Update Complete')

	def addMovie(self, MOVIE):
		for g in MOVIE.genres:
			if g not in self.listGenres:
				if g != '' and g != self.MISSING_DATA:
					(self.listGenres).append(g)

		self.movies.append(MOVIE)

	def newMovie(self, movie_title):
		# Add a new movie just with a movie title
		self.updateMovieDB(movie_title, len(self.movies) + 1)
		get_image(self.movies[-1].poster_path, self.movies[-1].title)
		self.loadDB()

	# The following are functions if info is being pulled from a Google Sheet

	def get_credentials(self):
		"""Gets valid user credentials from storage.

		If nothing has been stored, or if the stored credentials are invalid,
		the OAuth2 flow is completed to obtain the new credentials.

		Returns: Credentials, the obtained credential.
		"""
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
		credentials = get_credentials()
		http = credentials.authorize(httplib2.Http())
		discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
						'version=v4')
		service = discovery.build('sheets', 'v4', http=http,
									discoveryServiceUrl=discoveryUrl)

		# Pull data from the Google Sheet
		# self.spreadsheetID = '1OPg5wtyTFglYPGNYug4hDbHGGfo_yP9HOMRVjT29Lf8'
		self.spreadsheetID = sheetID
		rangeName = 'Sheet1!A:I'
		result = service.spreadsheets().values().get(
			spreadsheetId=self.spreadsheetID, range=rangeName).execute()
		values = result.get('values', [])

		# Add values to the Excel sheet
		book = xlwt.Workbook(encoding="utf-8")
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

		book.save("GoogleDocDB.xlsx")
		self.fileName = Database.location = "GoogleDocDB.xlsx"
		self.loadDB()

	def upload_google_doc(self):
		# Run Google OAuth2
		credentials = get_credentials()
		http = credentials.authorize(httplib2.Http())
		discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
						'version=v4')
		service = discovery.build('sheets', 'v4', http=http,
									discoveryServiceUrl=discoveryUrl)

		# self.spreadsheetId = '1OPg5wtyTFglYPGNYug4hDbHGGfo_yP9HOMRVjT29Lf8'

		# Open the Excel sheet to read in data
		workbook = xlrd.open_workbook('testing.xlsx', on_demand=True)
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
			spreadsheetId=self.spreadsheetId, range=range_name,
			valueInputOption='USER_ENTERED', body=body).execute() # USER_ENTERED or RAW


if __name__ == "__main__":
	db = Database()
	db.get_google_doc('1OPg5wtyTFglYPGNYug4hDbHGGfo_yP9HOMRVjT29Lf8')

	for movie in db.movies:
		print(movie.title)

	db.newMovie('Ben Hur')
	db.upload_google_doc()
