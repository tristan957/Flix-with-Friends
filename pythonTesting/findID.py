import tmdbsimple as tmdb
tmdb.API_KEY = 'b299f0e8dce095f8ebcbae6ab789005c'

search = tmdb.Search()

with open("Movies.csv") as f:
    content = f.readlines()

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

length = file_len("Movies.csv")

for i in range(length):
    a = content[i].split(",")
    print('CORRECT MOVIE NAME: ', a[0])

    # Search for info about Forest Gump
    response = search.movie(query=a[0])

    for s in search.results:
        print (s['title'])
        print(s['id'])
        # print( s['overview'])
        print('\n')


# response = search.movie(query='259316')



# # Search for info about Forest Gump
# response = search.movie(query='Saving Private Ryan')
#
# for s in search.results:
#     print (s['title'])
#     print(s['id'])
#     # print( s['overview'])
#     print('\n')
