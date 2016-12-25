import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib
from MovieDialog import MovieDialog
from Database import Database

class MovieHeaderBar(Gtk.HeaderBar):

	def __init__(self, reveal, searchBar):
		Gtk.HeaderBar.__init__(self, title = "Stop Bitchin', Start Watchin'", show_close_button = True)

		self.fileButton = Gtk.FileChooserButton()	#create a Gtk.FileChooserButton
		self.fileButton.connect("file-set", self.fileButton_cb)	#connects the file-set signal to fileButton_cb
		self.pack_start(self.fileButton)	#adds the button to the start of the headerbar

		#button to display popover displaying add/delete options to data
		self.dataIcon = Gio.ThemedIcon(name = "open-menu-symbolic")
		self.dataImage = Gtk.Image.new_from_gicon(self.dataIcon, Gtk.IconSize.BUTTON)

		self.addMovieButton = Gtk.ModelButton(label = "Add a Movie")
		self.addMovieButton.connect("clicked", self.manipulate_MovieButton_cb, "Add")
		self.deleteMovieButton = Gtk.ModelButton(label = "Delete a Movie")
		self.deleteMovieButton.connect("clicked", self.manipulate_MovieButton_cb, "Delete")
		self.dataBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		self.dataBox.add(self.addMovieButton)
		self.dataBox.add(self.deleteMovieButton)
		self.dataButton = Gtk.Button(image = self.dataImage)
		self.dataButton.connect("clicked", self.dataButton_cb)
		self.dataPopover = Gtk.PopoverMenu(position = Gtk.PositionType.BOTTOM, relative_to = self.dataButton)
		self.dataPopover.add(self.dataBox)
		self.pack_end(self.dataButton)

		self.randomMovieButton = Gtk.Button(label = "Random Movie")
		self.randomMovieButton.connect("clicked", self.randomMovieButton_cb)
		self.pack_end(self.randomMovieButton)

		self.searchIcon = Gio.ThemedIcon(name = "edit-find-symbolic")	#create an image to place on the button
		self.searchImage = Gtk.Image.new_from_gicon(self.searchIcon, Gtk.IconSize.BUTTON)
		self.searchButton = Gtk.ToggleButton(image = self.searchImage)	#creates a button with an image
		self.searchButton.connect("clicked", self.searchButton_cb, reveal, searchBar)	#connects the activate signal to searchButton_cb
		self.pack_end(self.searchButton)	#adds the button to the end of the headerbar

	#callback for when the fileButton is pressed
	def fileButton_cb(self, fileButton):
		filename = fileButton.get_filename()
		db = Database(filename)
		Database.location = filename

	def randomMovieButton_cb(self, randomMovieButton):
		print("Random Movie")

	#callback for when the searchButton is pressed
	def searchButton_cb(self, searchButton, reveal, searchBar):
		if searchButton.get_active() == True:
			reveal.set_transition_type(Gtk.RevealerTransitionType.SLIDE_DOWN)
			reveal.set_reveal_child(True)
			searchBar.entry.grab_focus()
		else:
			reveal.set_transition_type(Gtk.RevealerTransitionType.SLIDE_UP)
			reveal.set_reveal_child(False)
			self.grab_focus()

	def dataButton_cb(self, dataButton):
		self.dataPopover.show_all()

	def manipulate_MovieButton_cb(self, movieButton, action):
		manipulateDialog = MovieDialog(action)
		manipulateDialog.connect("delete-event", Gtk.main_quit)	#when delete-event signal is received, calls Gtk.main_quit
		manipulateDialog.show_all()	#display the window and all widgets
		Gtk.main()	#continuous function for running GTK applications
