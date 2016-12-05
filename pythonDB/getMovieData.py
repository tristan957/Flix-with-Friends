# This is a testing file

import sys
import tmdbsimple as tmdb
import urllib.request

tmdb.API_KEY = 'b299f0e8dce095f8ebcbae6ab789005c'

# Initialize the search for The movie database
search = tmdb.Search()

# Open the CSV file and read the lines
with open("Movies.csv") as f:
    content = f.readlines()

# Func for determining lines in the CSV file
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

# If there is an argument
if len(sys.argv) > 1:
    arguments = sys.argv
    a = " ".join(arguments[1:])
    response = search.movie(query=a)
    i = 0
    for s in search.results:
        i = 1 + i
        if i == 1:
            # titleMovie = s['title']
            titleID = s['id']
            # print(titleMovie, titleID)
            forrestGump = tmdb.Movies(titleID)
            response = forrestGump.info()
            print(response['title'])
            print('Runtime:', response['runtime'], 'minutes')
            # print('Runtime: ', response['rating'])
            print('Overview:', response['overview'])
            gen = response['genres']
            print('Genres:', end=' ')
            for i in range(0,len(gen)):
                print(gen[i]['name'], end=" ")
            print()
            print('Release Date:', response['release_date'])
            print('Vote Average: ', response['vote_average'], '/10',sep='')
            print('Popularity:',response['popularity'], 'million(s)')

            url300_450 = 'https://image.tmdb.org/t/p/w300_and_h450_bestv2'
            imagePage = url300_450 + response['poster_path']
            print('URL image:',imagePage)
            urllib.request.urlretrieve(imagePage, response['title'] + '.jpg')

            # print(response)

    if i == 0:
        print(a, 'not found')
else:

    # Utilize the function
    length = file_len("Movies.csv")

    # For all the movie titles before the delimitter, run a search and
    #   and use the first earch result's  movie ID to get info
    for i in range(length):
        a = content[i].split(",")
        print('CORRECT MOVIE: ', a[0])

        response = search.movie(query=a[0])
        i = 0
        for s in search.results:
            i = 1 + i
            if i == 1:
                titleID = s['id']
                daMovie = tmdb.Movies(titleID)
                response = daMovie.info()
                print(response['title'])
                print('Runtime: ', response['runtime'])
                print('Overview: ', response['overview'], '\n')

        if i == 0:
            print(a, 'not found')
