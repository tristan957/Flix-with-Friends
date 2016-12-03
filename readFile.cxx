#include "readFile.hxx"


void readFile(string file_name)
{
	ifstream file (file_name);
	if(!file) throw runtime_error("Failed to open file " + file_name);
	tring value;

	while ( file.good() )
	{
	 	getline ( file, value, ',' ); // read a string until next comma:
	    // cout << string( value, 0, value.length() ) << endl;
	}
}
