from Movie import Movie
from Database import Database
import MovieMain

def main():

    db = Database('testing.xlsx')

    for movie in db.movies:
        if movie.title == "A Beautiful Mind":
            print("FOUND IT")



if __name__ == "__main__":
    main()
