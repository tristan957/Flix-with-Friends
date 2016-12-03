#ifndef MOVIE_HXX
#define MOVIE_HXX

#include <string>
#include <vector>

using namespace std;

class Movie
{
private:
	string title;
	vector<string> genres;
	vector<string> actors;
	vector<string> sawers;

public:
	Movie(string title);
	Movie(string title, vector<string> genres, vector<string> actors, vector<string> sawers);

	string& get_title();
	vector<string>& get_genres();
	vector<string>& get_actors();
	vector<string>& get_sawers();
};

#endif
