# import openpyxl as xl
#
# workBook = xl.load_workbook('testing.xlsx')
#
# print(workBook.get_sheet_names())
#
# sheet = workBook.active
# print(sheet['A1'].value)

import xlwt
import xlrd
from xlutils.copy import copy
import tmdbsimple as tmdb
tmdb.API_KEY = 'b299f0e8dce095f8ebcbae6ab789005c'

def outputMovie(movie, row):
    search = tmdb.Search()
    response = search.movie(query=movie)
    i = 0
    for s in search.results:
        i = 1 + i
        if i == 1:
            titleID = s['id']
            daMovie = tmdb.Movies(titleID)
            response = daMovie.info()
            # print(response['title'])
            w_sheet.write(i,0,response['title'])
            # print('Runtime: ', response['runtime'])
            w_sheet.write(i,2,response['runtime'])
            # print('Overview: ', response['overview'], '\n')
            w_sheet.write(i,3,response['overview'])

    if i == 0:
        print(a, 'not found')
        w_sheet.write(i,0,'not found')
        # print('Runtime: ', response['runtime'])
        w_sheet.write(i,2,'not found')
        # print('Overview: ', response['overview'], '\n')
        w_sheet.write(i,3,'not found')




# Open the excel file
rb = xlrd.open_workbook('testing.xlsx')

# make a writeable copy of the open excel file
wb = copy(rb)

# read the frist sheet to write to within the writable copy
w_sheet = wb.get_sheet(0)

# write or modify the value at the first row - second column
# w_sheet.write(0,1,'ViewedBy')


outputMovie('Saving Private Ryan',1)

# save the workBook
wb.save('testing.xlsx')
