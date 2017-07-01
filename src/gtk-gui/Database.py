import pymongo
# import pprint
import tmdbsimple as tmdb

from Movie import Movie

tmdb.API_KEY = 'b299f0e8dce095f8ebcbae6ab789005c'


class Database:

    def __init__(self, cred_dict):
        # self.client = pymongo.MongoClient(DB_INFO['link'])
        self.client = pymongo.MongoClient('mongodb://test:test@ds133418.mlab.com:33418/flix_with_friends')
        # UNCOMMENT ME FOR PRES
        # self.client = pymongo.MongoClient('mongodb://' + cred_dict['username'] + ':' + cred_dict['password'] + '@' + cred_dict['location'])
        self.db = self.client.flix_with_friends
        self.movie_collection = self.db.movie_collection
        self.viewer_collection = self.db.viewer_collection
        self.movies = []
        self.listGenres = []
        self.oldest_year = 3000
        self.troubled_list = [] # array of movies with bad data
        self.movieTitles = []
        self.viewers = []

        self.get_from_db_movies(self.movie_collection)
        self.get_images()

        duplicate_movies = self.remove_duplicates()
        is_bad = False

        for num in duplicate_movies:
            is_bad = True
            print(self.movies[num].title)
            id = self.movies[num].db_id
            self.movie_collection.remove({"_id": id})

        if is_bad:
            self.movies = []
            self.movieTitles = []
            self.get_from_db_movies(self.movie_collection)

        self.movies.sort(key=lambda x: x.title)

    def get_from_db_movies(self, DB_COLLECTION):
        # need all movies as movie class
        # list of movie titles
        for item in DB_COLLECTION.find({}):
            movie_to_add = Movie(item)

            # Check if Movie has a new genre
            for g in movie_to_add.genres:
                if g not in self.listGenres:
                    if g != '':
                        self.listGenres.append(g)

            # Add Friend if Movie has a friend not accounted for
            for v in movie_to_add.viewers:
                if v not in self.viewers:
                    if v != '':
                        self.viewers.append(v)

            # Check if Movie has a new Oldest release year
            if movie_to_add.release_date[:4] < str(self.oldest_year):
                self.oldest_year = int(movie_to_add.release_date[:4])

            self.movies.append(movie_to_add)
        return self.movies

    def search_movie(self, MOVIE_QUERY, num=1):
        results = []
        count = 0
        search = tmdb.Search() # Setup search to run API query
        response = search.movie(query=MOVIE_QUERY)

        for s in search.results:
            titleID = s['id']
            m = Movie(self.get_movie_info(tmdb.Movies(titleID)))
            results.append(m)
            print(m.title)

            count = count + 1
            if count == num:
                return results

    def get_trailer(self, MOVIE):
        videos = MOVIE.videos()['results']
        for val in videos:
            if val['type'] == 'Trailer':
                return 'https://www.youtube.com/watch?v=' + val['key']

    def get_images(self):
        for m in self.movies:
            m.get_image()

    def remove_duplicates(self):
        seen = set()
        duplicate_movies = []
        i = 0
        for x in self.movies:
            if x.title in seen:
                duplicate_movies.append(i)
            seen.add(x.title)
            i += 1
        return duplicate_movies

    def get_movie_info(self, MOVIE):
        # Get Movie info as json object
        movie = MOVIE.info()

        # Delete unecessary API items
        deleteItems = ['original_title', 'vote_count', 'video', 'production_countries', 'production_companies', 'popularity', 'original_language', 'imdb_id', 'homepage', 'budget', 'belongs_to_collection', 'adult', 'spoken_languages', 'status']
        for item in deleteItems:
            del movie[item]

        # Format Genres Properly
        genres = []
        for item in movie['genres']:
            genres.append(item['name'])
        del movie['genres']

        # Get Actor and Director Info
        credits = MOVIE.credits()

        for person in credits['crew']:
            if person['job'] == 'Director':
                director_name = person['name']
                director_img = person['profile_path']
                break

        actor_name = []
        actor_char = []
        actor_img = []

        for i, person in enumerate(credits['cast']):
            actor_name.append(person['name'])
            actor_char.append(person['character'])
            actor_img.append(person['profile_path'])
            if i == 2:
                break

        # Keywords
        keywords_api = MOVIE.keywords()
        keywords = []

        for key in keywords_api['keywords']:
            keywords.append(key['name'])

        if 'keywords' in movie:
            movie['keywords'] = keywords
        if 'genres' in movie:
            movie['genres'] = genres
        if 'director_name' in movie:
            movie['director_name'] = director_name
        if 'director_img' in movie:
            movie['director_img'] = director_img
        if 'actor_name' in movie:
            movie['actor_name'] = actor_name
        if 'actor_char' in movie:
            movie['actor_char'] = actor_char
        if 'actor_img' in movie:
            movie['actor_img'] = actor_img
        if 'trailer' in movie:
            movie['trailer'] = self.get_trailer(MOVIE)
        return movie

    def add_movie_db(self, MOVIE_ID):
        movie = self.get_movie_info(tmdb.Movies(MOVIE_ID))
        movie['viewers'] = ''
        self.movie_collection.insert(movie)

    def find_movie(self, title):
        for movie in self.movies:
            if movie.title == title:
                return movie


if __name__ == '__main__':
    db = Database()
    for i, m in enumerate(db.movies):
        if m.title == 'Shrek':
            print(i)
