from Movie import Movie
from Database import Database


def main():
    # m = Movie('American Horror Story', 'NAN')
    # print(m.title)
    db = Database('testing.xlsx')
    # print(db.dictionary)
    # b = Movie(db.dictionary[0])
    # c = Movie(db.dictionary[1])
    # db.addMovie(b)
    # db.addMovie(c)
    for movie in db.movies:
        print(movie.title, '-', movie.overview, '\n')
    # print(b)
    # db.update()


if __name__ == "__main__":
    main()
