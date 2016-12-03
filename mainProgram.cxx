#include <exception>
#include <iostream>
#include <string>
#include <vector>
#include "menu.hxx"
#include "Movie.hxx"

using namespace std;

int main()
{
	cout << "Welcome to Movie Night Helper!" << endl;
	cout << "Version .2" << endl << endl;


	//if()
	//{
		//vector<Movies> list = read_file(file)
		bool menu = true;
		while(menu == true)
		{
			print_menu();
			/*cout << "1. Add a movie\n";
			cout << "2. Delete a movie\n";
			cout << "3. Search\n";
			cout << "4. Display information about all movies within a genre\n";
			cout << "5. Display information about all movies released in a certain year\n";
			cout << "6. Randomly generate a genre\n";
			cout << "7. Randomly generate a movie\n";
			cout << "8. Exit\n";*/
			try
			{
				int choice = get_input();
				switch(choice)
				{
					case 1:
					{
						break;
					}
					case 2:
					{
						break;
					}
					case 3:
					{
						break;
					}
					case 4:
					{
						break;
					}
					case 5:
					{
						break;
					}
					case 6:
					{
						break;
					}
					case 7:
					{
						break;
					}
					case 8:
					{
						break;
					}
				}
			}
			catch(runtime_error& e)
			{
				cerr << e.what() << endl << endl;
			}
		}
	//}
}
