# import tmdbsimple as tmdb
# tmdb.API_KEY = 'b299f0e8dce095f8ebcbae6ab789005c'
#
# api = tmdb.API(b299f0e8dce095f8ebcbae6ab789005c)
# api.movie(<parameters>)
#
# search = tmdb.Search()
# # response = search.movie(query='259316')
#
# # Search for info about Forest Gump
# response = search.movie(query='Forest Gump')
# for s in search.results:
#     with open('file.txt', 'w') as f:
#         print (s['title'], file=f)
#         # print(s['id'], s['release_date'], s['popularity'], file=f)
#         print(s['popularity'], file =f)
#         print( s['overview'], file=f)
#         print('\n\n\n',file=f)
#
# response = search.movie(movie_id='13')
# for s in search.results:
#     with open('file.txt', 'a') as f:
#         print (s['title'], file=f)
#         # print(s['id'], s['release_date'], s['popularity'], file=f)
#         print(s['popularity'], file =f)
#         print( s['overview'], file=f)

from tmdb import set_key
set_key('b299f0e8dce095f8ebcbae6ab789005c')
