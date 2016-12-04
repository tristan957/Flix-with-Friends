import tmdbsimple as tmdb
tmdb.API_KEY = 'b299f0e8dce095f8ebcbae6ab789005c'

search = tmdb.Search()

with open("Movies.csv") as f:
    content = f.readlines()

j = 0
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

length = file_len("Movies.csv")

for i in range(length):
    a = content[i].split(",")
    print('CORRECT MOVIE: ', a[0])

    # Search for info about Forest Gump

    response = search.movie(query=a[0])

    i = 0
    for s in search.results:
        i = 1+i
        if i == 1:
            j = j+1
            # titleMovie = s['title']
            titleID = s['id']
            # print(titleMovie, titleID)
            forrestGump = tmdb.Movies(titleID)
            response = forrestGump.info()
            print(response['title'])
            print('Runtime: ', response['runtime'])
            print('Overview: ', response['overview'])
            print(j)

            print('\n')


# 
# # Forrest Gump
# forrestGump = tmdb.Movies(13)
# response = forrestGump.info()
# print(response['title'])
#
# # Saving Private Ryan
# savingPrivateRyan = tmdb.Movies(857)
# savingPrivateRyanInfo = savingPrivateRyan.info()
# print(savingPrivateRyanInfo['title'])
#
# # Dead Poet Society
#
# # Mulan
#
# # Shrek
#
# # P.S. I love You
