#include "Movie.hxx"

Movie::Movie() {}

Movie::Movie(string title)
{
	this -> title = title;
}

Movie::Movie(string title, vector<string> genres, vector<string> actors, vector<string> viewers)
{
	this -> title = title;
	this -> genres = genres;
	this -> actors = actors;
	this -> viewers = viewers;
}

string& Movie::get_title()
{
	return title;
}

vector<string>& Movie::get_genres()
{
	return genres;
}

vector<string>& Movie::get_actors()
{
	return actors;
}

vector<string>& Movie::get_viewers()
{
	return viewers;
}

// Input data from csv
istream& operator>>(istream& is, Movie& m) {
	// is >> m.title >> m.push_back(genres) >> m.push_back(actors);

	// string title;
	// vector<string> genres;
	// vector<string> actors;
	// vector<string> viewers;

	return is;
}

// Extract info about movie
ostream& operator<<(ostream& os, const Movie& m) {
	// os <<

	return os;
}
