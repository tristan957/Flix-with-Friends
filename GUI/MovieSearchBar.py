import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MovieSearchBar(Gtk.Box):
	#needs a grid of GtkToggleButtons
	def __init__(self):
		Gtk.Box.__init__(self, orientation = Gtk.Orientation.HORIZONTAL, spacing = 50)

		self.categories = []

		self.search = Gtk.SearchBar(search_mode_enabled = True, show_close_button = True)
		self.entry = Gtk.SearchEntry()
		self.search.connect_entry(self.entry)
		self.entry.grab_focus()
		self.pack_start(self.entry, True, True, 0)

		self.nameButton = Gtk.ToggleButton(label = "Name")
		self.descriptionButton = Gtk.ToggleButton(label = "Description")
		self.genreButton = Gtk.ToggleButton(label = "Genre")
		self.yearButton = Gtk.ToggleButton(label = "Year of Release")
		self.unviewedButton = Gtk.ToggleButton(label = "Unviewed")

		self.buttonBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 5)
		self.buttonBox.pack_start(self.nameButton, True, True, 0)
		self.buttonBox.pack_start(self.descriptionButton, True, True, 0)
		self.buttonBox.pack_start(self.genreButton, True, True, 0)
		self.buttonBox.pack_start(self.yearButton, True, True, 0)
		self.buttonBox.pack_start(self.unviewedButton, True, True, 0)

		self.nameButton.connect("toggled", self.searchCategories_cb)
		self.descriptionButton.connect("toggled", self.searchCategories_cb)
		self.genreButton.connect("toggled", self.searchCategories_cb)
		self.yearButton.connect("toggled", self.searchCategories_cb)
		self.unviewedButton.connect("toggled", self.searchCategories_cb)

		self.pack_start(self.buttonBox, True, True, 0)

	def searchCategories_cb(self, searchButton):
		if searchButton.get_active() == True:
			self.categories.append(searchButton.get_label())
		else:
			self.categories.remove(searchButton.get_label())

	def getCategories(self):
		return self.categories
