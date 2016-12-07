from Movie import Movie
from Database import Database

def main():
    m = Movie('American Horror Story')
    print(m.title)
    db = Database('testing.xlsx')
    print(db.dictionary[0]['Title'])
    db.update()





if __name__ == "__main__":
    main()
