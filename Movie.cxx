#include "Movie.hxx"

Movie::Movie(string title)
{
	this -> title = title;
}

Movie::Movie(string title, vector<string> genres, vector<string> actors, vector<string> sawers)
{
	this -> title = title;
	this -> genres = genres;
	this -> actors = actors;
	this -> sawers = sawers;
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

vector<string>& Movie::get_sawers()
{
	return sawers;
}
