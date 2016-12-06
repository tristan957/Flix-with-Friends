import DB

# DB.update(DB.DATABASE)

class Movie:
    # Public variables - could be wrong, making class similiar to c++
    title = ''
    viewers = []
    runtime = 0
    genres = []
    release_date = ''
    vote = 0
    overview = ''

    def __init__(self, tI = '', vI = [], rU = 0, gE = []
                , rD = '', vO = 0, oV = ''):
        self.title = tI
        self.viewers = vI
        self.runtime = rU
        self.genres = gE
        self.release_date = rD
        self.vote = vO
        self.overview = oV






# # TESTING GROUNDS
# m = Movie('American Horror Story', ['Joseph', 'Tristan'])
#
#
# print(m.viewers)
