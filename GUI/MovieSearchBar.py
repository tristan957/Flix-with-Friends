import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MovieSearchBar(Gtk.Box):
	#needs a grid of GtkToggleButtons
	def __init__(self):
		Gtk.Box.__init__(self, orientation = Gtk.Orientation.HORIZONTAL, spacing = 100)

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

		self.buttonBox = Gtk.Box()
		self.buttonBox.pack_start(self.nameButton, True, True, 0)
		self.buttonBox.pack_start(self.descriptionButton, True, True, 0)
		self.buttonBox.pack_start(self.genreButton, True, True, 0)
		self.buttonBox.pack_start(self.yearButton, True, True, 0)
		self.buttonBox.pack_start(self.unviewedButton, True, True, 0)
		self.pack_start(self.buttonBox, True, True, 0)
