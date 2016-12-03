#include "readFile.hxx"
#include <vector>


void readFile(string file_name)
{
  ifstream file (file_name);
  if(!file) throw runtime_error("Failed to open file " + file_name);
  tring value;
  string value;
  vector<string> test;


  while ( file.good() )
  {
     getline ( file, value, ',' ); // read a string until next comma:
      // cout << string( value, 0, value.length() ) << endl;

    // If cell has multible values
    if (value[0] == '"' )
    {
      int startVal = 1;
      string temp = value;
      while (temp[0] = ' ')
      {
        temp = value.substr(startVal,value.find(","));
        test.push_back(temp);
        std::cout << value;
        startVal = value.find(",") + 1;
      }
      for (int i = 0; i < test.size(); i++) {
        std::cout << test.at(i) << '\n';
      }
    } else
    {
      cout <<  value << endl;
    }
  }
} 
