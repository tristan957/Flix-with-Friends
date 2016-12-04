import sys
import tmdbsimple as tmdb
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




if len(sys.argv) > 1:
    arguments = sys.argv
    a = " ".join(arguments[1:])
    # print(a)
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
            print('Runtime: ', response['runtime'])
            print('Overview: ', response['overview'], '\n')

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
                # titleMovie = s['title']
                titleID = s['id']
                # print(titleMovie, titleID)
                forrestGump = tmdb.Movies(titleID)
                response = forrestGump.info()
                print(response['title'])
                print('Runtime: ', response['runtime'])
                print('Overview: ', response['overview'], '\n')
