#ifndef MOVIE_HXX
#define MOVIE_HXX

#include <string>
#include <iostream>
#include <vector>

using namespace std;

class Movie
{
private:
	string title;
	vector<string> genres;
	vector<string> actors;
	vector<string> viewers;

	friend istream& operator>>(istream& is, Movie& m);
public:
	Movie();
	Movie(string title);
	Movie(string title, vector<string> genres, vector<string> actors, vector<string> viewers);

	string& get_title();
	vector<string>& get_genres();
	vector<string>& get_actors();
	vector<string>& get_viewers();
};


ostream& operator<<(ostream& os, const Movie& m);

#endif
