#include "menu.hxx"

void print_menu()
{
	cout << "1. Add a movie\n";
	cout << "2. Delete a movie\n";
	cout << "3. Search\n";
	cout << "4. Display information about all movies within a genre\n";
	cout << "5. Display information about all movies released in a certain year\n";
	cout << "6. Randomly generate a genre\n";
	cout << "7. Randomly generate a movie\n";
	cout << "8. Exit\n";
}

int get_input()
{
	cout << "Enter a selection: ";
	int choice;
	if(cin >> choice && choice >= 1 && choice <= 8)
	{
		return choice;
	}
	else
	{
		cin.clear();
		cin.ignore(numeric_limits<streamsize>::max(), '\n');
		throw runtime_error("Bad input. Integer between 1-8 expected.");
	}
}
