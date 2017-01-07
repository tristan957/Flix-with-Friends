import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib
from MovieDialog import MovieDialog
from FriendDialog import FriendDialog
from Database import Database

class MovieHeaderBar(Gtk.HeaderBar):

	def __init__(self, parent, reveal, searchBar):
		Gtk.HeaderBar.__init__(self, title = "Flix with Friends", show_close_button = True)

		# button to display popover displaying add/delete options to data
		self.dataIcon = Gio.ThemedIcon(name = "open-menu-symbolic")
		self.dataImage = Gtk.Image.new_from_gicon(self.dataIcon, Gtk.IconSize.BUTTON)

		self.addMovieButton = Gtk.ModelButton(label = "Add a Movie")
		self.addMovieButton.connect("clicked", self.manipulateMovieButton_cb, parent, "Add")
		self.deleteMovieButton = Gtk.ModelButton(label = "Delete a Movie")
		self.deleteMovieButton.connect("clicked", self.manipulateMovieButton_cb, parent, "Delete")
		self.dataSeparator = Gtk.Separator.new(Gtk.Orientation.HORIZONTAL)
		self.addFriendButton = Gtk.ModelButton(label = "Add a Friend")
		self.addFriendButton.connect("clicked", self.manipulateFriend_cb, parent, "Add")
		self.deleteFriendButton = Gtk.ModelButton(label = "Delete a Friend")
		self.deleteFriendButton.connect("clicked", self.manipulateFriend_cb, parent, "Delete")
		self.dataBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		self.dataBox.add(self.addMovieButton)
		self.dataBox.add(self.deleteMovieButton)
		self.dataBox.add(self.dataSeparator)
		self.dataBox.add(self.addFriendButton)
		self.dataBox.add(self.deleteFriendButton)
		self.dataPopover = Gtk.PopoverMenu(position = Gtk.PositionType.BOTTOM)  # , relative_to = self.dataButton)
		self.dataPopover.add(self.dataBox)
		self.dataButton = Gtk.MenuButton(image = self.dataImage, use_popover = True, popover = self.dataPopover)
		self.dataButton.connect("clicked", self.dataButton_cb)
		self.pack_end(self.dataButton)

		self.randomMovieButton = Gtk.Button(label = "Random Movie")
		self.randomMovieButton.connect("clicked", self.randomMovieButton_cb)
		self.pack_start(self.randomMovieButton)

		self.searchIcon = Gio.ThemedIcon(name = "edit-find-symbolic")  # create an image to place on the button
		self.searchImage = Gtk.Image.new_from_gicon(self.searchIcon, Gtk.IconSize.BUTTON)
		self.searchButton = Gtk.ToggleButton(image = self.searchImage)  # creates a button with an image
		self.searchButton.connect("clicked", self.searchButton_cb, reveal, searchBar)  # connects the activate signal to searchButton_cb
		self.pack_end(self.searchButton)  # adds the button to the end of the headerbar

	# callback for when the fileButton is pressed
	def fileButton_cb(self, fileButton):
		filename = fileButton.get_filename()
		db = Database(filename)
		Database.location = filename

	def randomMovieButton_cb(self, randomMovieButton):
		print("Random Movie")

	# callback for when the searchButton is pressed
	def searchButton_cb(self, searchButton, reveal, searchBar):
		if searchButton.get_active() is True:
			reveal.set_transition_type(Gtk.RevealerTransitionType.SLIDE_DOWN)
			reveal.set_reveal_child(True)
			searchBar.searchEntry.grab_focus()
		else:
			reveal.set_transition_type(Gtk.RevealerTransitionType.SLIDE_UP)
			reveal.set_reveal_child(False)
			self.grab_focus()

	def dataButton_cb(self, dataButton):
		self.dataPopover.show_all()

	def manipulateMovieButton_cb(self, movieButton, parent, action):
		manipulateDialog = MovieDialog(parent, action)

	def manipulateFriend_cb(self, friendButton, parent, action):
		manipulateDialog = FriendDialog(parent, action)
