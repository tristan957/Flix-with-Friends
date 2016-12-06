from Movie import Movie
from Database import Database

def main():
    m = Movie('American Horror Story')
    print(m.title)
    db = Database('testing.xlsx')
    db.createDictionary()
    print(db.dictionary[0]['Title'])





if __name__ == "__main__":
    main()
