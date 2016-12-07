import xlwt
import xlrd
from xlutils.copy import copy
from Movie import Movie
import tmdbsimple as tmdb
tmdb.API_KEY = 'b299f0e8dce095f8ebcbae6ab789005c'


class Database:

    def __init__(self, FN):
        self.fileName = ''
        self.dictionary = []  # cellular array of Excel file
        self.movies = []  # array of movies as class Movies
        self.fileName = FN
        self.loadDB()

    def loadDB(self):
        self.createDictionary()

        for movie in self.dictionary:
            self.addMovie(Movie(movie))
            # print(movie[0])

    def createDictionary(self):
        # This method converts all the data in the excelDB into a Listed PY dictionary
        # Access data by self.dictionary[row]['columnName']
        workbook = xlrd.open_workbook(self.fileName)
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
        # This method updates all columns of a movie in the DB
        rb = xlrd.open_workbook(self.fileName)  # Open the excel file
        wb = copy(rb)  # make a writeable copy of the open excel file
        w_sheet = wb.get_sheet(0)  # read the frist sheet to write to
        search = tmdb.Search()
        response = search.movie(query=movie)  # Search for movie
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
                w_sheet.write(row, 3, gen)
                w_sheet.write(row, 4, response['release_date'])
                w_sheet.write(row, 5, response['vote_average'])
                w_sheet.write(row, 6, response['overview'])
        if i == 0:  # If no search results
            print(movie, 'NOT FOUND')  # Print to console
            w_sheet.write(row, 2, 'NOT FOUND')
            w_sheet.write(row, 3, 'NOT FOUND')
            w_sheet.write(row, 4, 'NOT FOUND')
            w_sheet.write(row, 5, 'NOT FOUND')
            w_sheet.write(row, 6, 'NOT FOUND')

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
        self.movies.append(MOVIE)
