import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib
from MovieDialog import MovieDialog
from FriendDialog import FriendDialog
from Database import Database


class HeaderBar(Gtk.HeaderBar):

	def __init__(self, parent):
		"""Creates a header bar"""
		Gtk.HeaderBar.__init__(self, title = "Flix with Friends", show_close_button = True)

		self.parent = parent

		self.db = Database(Database.fileName)

		# button to display popover displaying add/delete options to data
		dataIcon = Gio.ThemedIcon(name = "open-menu-symbolic")
		dataImage = Gtk.Image.new_from_gicon(dataIcon, Gtk.IconSize.BUTTON)

		newSource = Gtk.ModelButton(label = "Change Source") # change the source of the database
		dataSeparator = Gtk.Separator.new(Gtk.Orientation.HORIZONTAL)
		addMovieButton = Gtk.ModelButton(text = "Add a Movie")
		addMovieButton.connect("clicked", self.manipulateMovies_cb, "Add")
		deleteMovieButton = Gtk.ModelButton(text = "Delete a Movie")
		deleteMovieButton.connect("clicked", self.manipulateMovies_cb, "Delete")
		dataSeparator = Gtk.Separator.new(Gtk.Orientation.HORIZONTAL)
		addFriendButton = Gtk.ModelButton(text = "Add a Friend")
		addFriendButton.connect("clicked", self.manipulateFriends_cb, "Add")
		deleteFriendButton = Gtk.ModelButton(text = "Delete a Friend")
		deleteFriendButton.connect("clicked", self.manipulateFriends_cb, "Delete")

		dataBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		dataBox.add(newSource)
		dataBox.add(addMovieButton)
		dataBox.add(deleteMovieButton)
		dataBox.add(dataSeparator)
		dataBox.add(addFriendButton)
		dataBox.add(deleteFriendButton)

		self.dataPopover = Gtk.PopoverMenu(position = Gtk.PositionType.BOTTOM)
		self.dataPopover.add(dataBox)
		dataButton = Gtk.MenuButton(image = dataImage, use_popover = True, popover = self.dataPopover)
		dataButton.connect("clicked", self.dataButton_cb)
		self.pack_end(dataButton)

		self.randomMovieButton = Gtk.Button(label = "Random Movie")
		self.randomMovieButton.get_style_context().add_class("suggested-action")
		self.randomMovieButton.connect("clicked", parent.searchBar.randomMovieButton_cb, parent)
		self.pack_start(self.randomMovieButton)

		searchIcon = Gio.ThemedIcon(name = "edit-find-symbolic")
		searchImage = Gtk.Image.new_from_gicon(searchIcon, Gtk.IconSize.BUTTON)
		self.searchButton = Gtk.ToggleButton(image = searchImage)
		self.searchButton.connect("clicked", self.searchButton_cb)
		self.pack_end(self.searchButton)

	def searchButton_cb(self, searchButton):
		"""Operates the search bar and search button in series"""
		if searchButton.get_active() is True:
			self.parent.searchBar.set_transition_type(Gtk.RevealerTransitionType.SLIDE_DOWN)
			self.parent.searchBar.set_reveal_child(True)
			if self.parent.searchBar.searchEntry.has_focus() is False:
				self.parent.searchBar.searchEntry.grab_focus()
		else:
			self.parent.searchBar.set_transition_type(Gtk.RevealerTransitionType.SLIDE_UP)
			self.parent.searchBar.set_reveal_child(False)
			self.grab_focus()

	def dataButton_cb(self, dataButton):
		self.dataPopover.show_all()

	def manipulateMovies_cb(self, movieButton, action):
		manipulateDialog = MovieDialog(self.parent, action)

	def manipulateFriends_cb(self, friendButton, parent, action):
		manipulateDialog = FriendDialog(self.parent, action)
