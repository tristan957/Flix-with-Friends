import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib

class MovieHeaderBar(Gtk.HeaderBar):

	def __init__(self):
		Gtk.HeaderBar.__init__(self, title = "Stop Bitchin', Start Watchin'", show_close_button = True)

		self.fileButton = Gtk.FileChooserButton()	#create a Gtk.FileChooserButton
		self.fileButton.connect("file-set", self.fileButton_cb)	#connects the file-set signal to fileButton_cb
		self.pack_start(self.fileButton)	#adds the button to the start of the headerbar

		#button to display popover displaying add/delete options to data
		dataIcon = Gio.ThemedIcon(name = "open-menu-symbolic")
		dataImage = Gtk.Image.new_from_gicon(dataIcon, Gtk.IconSize.BUTTON)

		addMovieButton = Gtk.ModelButton(label = "Add a Movie")
		deleteMovieButton = Gtk.ModelButton(label = "Delete a Movie")
		dataBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		dataBox.add(addMovieButton)
		dataBox.add(deleteMovieButton)
		self.dataButton = Gtk.Button(image = dataImage)
		self.dataButton.connect("clicked", self.dataButton_cb)
		self.dataPopover = Gtk.PopoverMenu(position = Gtk.PositionType.BOTTOM, relative_to = self.dataButton)
		self.dataPopover.add(dataBox)
		self.pack_end(self.dataButton)

		self.randomMovieButton = Gtk.Button(label = "Random Movie")
		self.randomMovieButton.connect("clicked", self.randomMovieButton_cb)
		self.pack_end(self.randomMovieButton)

		self.searchIcon = Gio.ThemedIcon(name = "edit-find-symbolic")	#create an image to place on the button
		self.searchImage = Gtk.Image.new_from_gicon(self.searchIcon, Gtk.IconSize.BUTTON)
		self.searchButton = Gtk.Button(image = self.searchImage)	#creates a button with an image
		self.searchButton.connect("clicked", self.searchButton_cb)	#connects the activate signal to searchButton_cb
		self.pack_end(self.searchButton)	#adds the button to the end of the headerbar

	#callback for when the fileButton is pressed
	def fileButton_cb(self, fileButton):
		filename = fileButton.get_filename()

	def randomMovieButton_cb(self, randomMovieButton):
		print("Random Movie")

	#callback for when the searchButton is pressed
	def searchButton_cb(self, searchButton):
		print("Search")

	def dataButton_cb(self, dataButton):
		self.dataPopover.show_all()
