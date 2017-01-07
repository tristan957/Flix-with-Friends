import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from MovieHeaderBar import MovieHeaderBar
from MovieSearchBar import MovieSearchBar
from MovieBox import MovieBox
from FileChooserBox import FileChooserBox

class MovieWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title = "Flix with Friends")

		self.createFileChooser()

	def createFileChooser(self):
		self.header = Gtk.HeaderBar(title = "Flix with Friends", show_close_button = True)
		self.set_titlebar(self.header)

		self.chooser = FileChooserBox(self)
		self.chooser.google.connect("clicked", self.google_cb)
		self.chooser.local.connect("clicked", self.local_cb)
		self.add(self.chooser)

	def createMovieFramework(self, location):
		self.box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		self.searchBar = MovieSearchBar(location)
		self.reveal = Gtk.Revealer(child = self.searchBar, transition_duration = 500)
		self.box.add(self.reveal)
		self.imdbBox = MovieBox()
		self.box.add(self.imdbBox)
		self.add(self.box)
		self.header = MovieHeaderBar(self, self.reveal, self.searchBar)	 # create headerbar
		self.set_titlebar(self.header)  # add it to the window
		self.connect("key-press-event", self.key_pressed_cb, self.reveal, self.searchBar, self.header)

		self.show_all()

	def key_pressed_cb(self, win, event, reveal, searchBar, header):
		reveal.set_transition_type(Gtk.RevealerTransitionType.SLIDE_DOWN)
		header.searchButton.set_active(True)
		reveal.set_reveal_child(True)
		return self.searchBar.search.handle_event(event)

	def google_cb(self, google):
		print(google.get_label())

	def local_cb(self, local):
		fileChooser = Gtk.FileChooserDialog(self, title = "Choose a Spreadsheet")
		fileChooser.add_button("Open", Gtk.FileChooserAction.OPEN)
		fileChooser.add_button("Cancel", Gtk.ResponseType.CANCEL)
		fileChooser.set_transient_for(self)
		fileChooser.connect("file_activated", self.doubleClickEnter_cb)
		if fileChooser.run() is 0:
			location = fileChooser.get_filename()

		fileChooser.destroy()
		self.remove(self.chooser)
		self.createMovieFramework(location)

	def doubleClickEnter_cb(self, fileChooser):
		location = fileChooser.get_filename()

		fileChooser.destroy()

		self.remove(self.chooser)
		self.createMovieFramework(location)
