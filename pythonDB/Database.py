import xlwt
import xlrd
from xlutils.copy import copy
from Movie import Movie
import tmdbsimple as tmdb
tmdb.API_KEY = 'b299f0e8dce095f8ebcbae6ab789005c'

class Database:
    fileName = ''
    dictionary = []

    def __init__(self, FN):
        Database.fileName = FN

    def createDictionary(self):
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
            Database.dictionary.append(elm)
            # This Database.dictionary has converted all the data in the excelDB into a Listed PY dictionary
            # Access data by dbName.dictionary[row]['columnName']
