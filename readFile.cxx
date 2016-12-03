#include "readFile.hxx"
#include <vector>


void readFile(string file_name)
{
  ifstream file (file_name);
  if(!file) throw runtime_error("Failed to open file " + file_name);
  string value;
  string temp;
  vector<string> test;

  while ( file.good() )
   {
     	getline ( file, value, ',' ); // read a string until next comma:
      	// cout << string( value, 0, value.length() ) << endl;

	    // If cell has multible values
	    if (value[0] == '"' )
	    {
			getline ( file, temp, ',' );
			value.append(",");
			value.append(temp);
	  	}

		std::cout << value << '\n';
	}
}
