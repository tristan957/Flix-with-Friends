import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from MovieHeaderBar import MovieHeaderBar
from MovieSearchBar import MovieSearchBar
from MovieBox import MovieBox
from Database import Database


class FileChooserBox(Gtk.Box):

	def __init__(self):
		Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL, spacing = 50)

		self.buttonBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 50)
		self.google = Gtk.Button(label = "Google Sheet")
		self.label = Gtk.Label("<big>Choose the location of your file</big>", use_markup = True)
		self.local = Gtk.Button(label = "Local Spreadsheet")
		self.buttonBox.add(self.google)
		self.buttonBox.add(self.local)
		self.add(self.label)
		self.add(self.buttonBox)

class MovieWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self)

		header = Gtk.HeaderBar(title = "Flix with Friends", show_close_button = True)	 # create headerbar
		self.set_titlebar(header)  # add it to the window

		self.main_stack = Gtk.Stack(transition_type = Gtk.StackTransitionType.SLIDE_UP_DOWN)
		# self.pack_start(self.main_stack, True, True, 0)
		self.add(self.main_stack)

		self.filePage = FileChooserBox()
		self.filePage.google.connect("clicked", self.google_cb)
		self.filePage.local.connect("clicked", self.local_cb)
		self.main_stack.add_named(self.filePage, "file-chooser")

		self.show_all()

	def key_pressed_cb(self, win, event):
		self.reveal.set_transition_type(Gtk.RevealerTransitionType.SLIDE_DOWN)
		self.header.searchButton.set_active(True)
		self.reveal.set_reveal_child(True)
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
			# Database.location = fileChooser.get_filename()
			Database.location = 'testing.xlsx' # TEMP
			self.addMovieStack(Database.location)
			self.main_stack.set_visible_child_name("movies")
		fileChooser.destroy()

	def doubleClickEnter_cb(self, fileChooser):
		# Database.location = fileChooser.get_filename()
		Database.location = 'testing.xlsx' # TEMP
		fileChooser.destroy()
		self.addMovieStack(Database.location)
		self.main_stack.set_visible_child_name("movies")

	def addMovieStack(self, location):
		box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		self.searchBar = MovieSearchBar(location)
		self.reveal = Gtk.Revealer(child = self.searchBar, transition_duration = 300)
		box.add(self.reveal)
		self.imdbBox = MovieBox()
		box.add(self.imdbBox)

		self.header = MovieHeaderBar(self, self.reveal, self.searchBar)
		self.set_titlebar(self.header)
		self.connect("key-press-event", self.key_pressed_cb)

		self.main_stack.add_named(box, "movies")
		self.show_all()
