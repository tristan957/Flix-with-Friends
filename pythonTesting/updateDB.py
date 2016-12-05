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

# Excel name for DB
DATABASE = 'testing.xlsx'

def outputMovie(file, movie, row):
    # Open the excel file - probaly what takes so long
    rb = xlrd.open_workbook(file)
    # make a writeable copy of the open excel file
    wb = copy(rb)
    # read the frist sheet to write to within the writable copy
    w_sheet = wb.get_sheet(0)
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
            w_sheet.write(row,0,response['title'])
            # print('Runtime: ', response['runtime'])
            w_sheet.write(row,2,response['runtime'])
            # print('Release Date:', response['release_date'])
            w_sheet.write(row,4,response['release_date'])
            w_sheet.write(row,5,response['vote_average'])
            # print('Overview: ', response['overview'], '\n')
            w_sheet.write(row,6,response['overview'])

    if i == 0:
        print(movie, 'not found')
        # print('Runtime: ', response['runtime'])
        w_sheet.write(row,2,'not found')
        # print('Overview: ', response['overview'], '\n')
        w_sheet.write(row,3,'not found')

    wb.save('testing.xlsx')





# write or modify the value at the first row - second column
# w_sheet.write(0,1,'ViewedBy')

workbook = xlrd.open_workbook(DATABASE)
workbook = xlrd.open_workbook(DATABASE, on_demand = True)
worksheet = workbook.sheet_by_index(0)
first_row = [] # The row where we stock the name of the column
for col in range(worksheet.ncols):
    first_row.append( worksheet.cell_value(0,col) )
# transform the workbook to a list of dictionaries
data =[]
for row in range(1, worksheet.nrows):
    elm = {}
    for col in range(worksheet.ncols):
        elm[first_row[col]]=worksheet.cell_value(row,col)
    data.append(elm)
print(data)


# Update all info about Movies
for i,Movie in enumerate(data):
    outputMovie(DATABASE,Movie['Title'],i+1)
    print(Movie['Title'],i)

# save the workBook
