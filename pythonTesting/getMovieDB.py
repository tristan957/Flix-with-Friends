import tmdbsimple as tmdb
tmdb.API_KEY = 'b299f0e8dce095f8ebcbae6ab789005c'

# Forrest Gump
forrestGump = tmdb.Movies(13)
response = forrestGump.info()
print(response['title'])

# Saving Private Ryan
savingPrivateRyan = tmdb.Movies(857)
savingPrivateRyanInfo = savingPrivateRyan.info()
print(savingPrivateRyanInfo['title'])

# Dead Poet Society

# Mulan

# Shrek

# P.S. I love You
