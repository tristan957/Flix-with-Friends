import xlwt
import xlrd
from xlutils.copy import copy
import tmdbsimple as tmdb
tmdb.API_KEY = 'b299f0e8dce095f8ebcbae6ab789005c'

# TODO: need to change how it updates the entire base to, update if not a registered movie in the DB
# TODO: need to add images if not already present for different dimentions

# Excel filename for DB
DATABASE = 'testing.xlsx'


def outputMovie(file, movie, row):
    rb = xlrd.open_workbook(file)  # Open the excel file
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
            for i in range(0,len(genreResult)):
                gen += genreResult[i]['name']
                if i < (len(genreResult)-1):
                    gen += ', '
            # Write info to appropriate (row,column)
            w_sheet.write(row, 0, response['title'])
            w_sheet.write(row, 2, response['runtime'])
            w_sheet.write(row, 3, gen)
            w_sheet.write(row, 4, response['release_date'])
            w_sheet.write(row, 5, response['vote_average'])
            w_sheet.write(row, 6, response['overview'])
    if i == 0:  # If no search results
        print(movie, 'not found')  # Print to console
        w_sheet.write(row, 2, 'not found')
        w_sheet.write(row, 4, 'not found')
        w_sheet.write(row, 5, 'not found')
        w_sheet.write(row, 6, 'not found')

    wb.save(file)  # Save DB edits


def getDict(DBfilename):
    # This function converts all the data in the DB into a PY dictionary
    workbook = xlrd.open_workbook(DBfilename)
    workbook = xlrd.open_workbook(DBfilename, on_demand=True)
    worksheet = workbook.sheet_by_index(0)
    first_row = []  # The row where we stock the name of the column
    for col in range(worksheet.ncols):
        first_row.append(worksheet.cell_value(0, col))
    # transform the workbook to a list of dictionaries
    data = []
    for row in range(1, worksheet.nrows):
        elm = {}
        for col in range(worksheet.ncols):
            elm[first_row[col]] = worksheet.cell_value(row, col)
        data.append(elm)
    return data


def update(DBfilename):
    data = {}
    data = getDict(DBfilename)
    # Update all info about Movies
    for i, Movie in enumerate(data):
        outputMovie(DATABASE, Movie['Title'], i + 1)
        print(Movie['Title'], i)


if __name__ == "__main__":
    update(DATABASE)
