import gi
import random
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib
from MovieDialog import MovieDialog
from FriendDialog import FriendDialog
from Database import Database


class MovieHeaderBar(Gtk.HeaderBar):

	def __init__(self, parent):
		Gtk.HeaderBar.__init__(self, title = "Flix with Friends", show_close_button = True)

		self.db = Database(Database.fileName)

		# button to display popover displaying add/delete options to data
		self.dataIcon = Gio.ThemedIcon(name = "open-menu-symbolic")
		self.dataImage = Gtk.Image.new_from_gicon(self.dataIcon, Gtk.IconSize.BUTTON)

		self.addMovieButton = Gtk.ModelButton(text = "Add a Movie")
		self.addMovieButton.connect("clicked", self.manipulateMovieButton_cb, parent, "Add")
		self.deleteMovieButton = Gtk.ModelButton(text = "Delete a Movie")
		self.deleteMovieButton.connect("clicked", self.manipulateMovieButton_cb, parent, "Delete")
		self.dataSeparator = Gtk.Separator.new(Gtk.Orientation.HORIZONTAL)
		self.addFriendButton = Gtk.ModelButton(text = "Add a Friend")
		self.addFriendButton.connect("clicked", self.manipulateFriend_cb, parent, "Add")
		self.deleteFriendButton = Gtk.ModelButton(text = "Delete a Friend")
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

		backIcon = Gio.ThemedIcon(name = "go-previous-symbolic")
		backImage = Gtk.Image.new_from_gicon(backIcon, Gtk.IconSize.BUTTON)
		self.back = Gtk.Button(image = backImage)
		forwardIcon = Gio.ThemedIcon(name = "go-next-symbolic")
		forwardImage = Gtk.Image.new_from_gicon(forwardIcon, Gtk.IconSize.BUTTON)
		self.forward = Gtk.Button(image = forwardImage)
		self.pack_start(self.back)
		self.pack_start(self.forward)

		self.randomMovieButton = Gtk.Button(label = "Random Movie")
		self.randomMovieButton.get_style_context().add_class("suggested-action")
		random.seed()
		self.randomMovieButton.connect("clicked", self.randomMovieButton_cb)
		self.pack_start(self.randomMovieButton)

		self.searchIcon = Gio.ThemedIcon(name = "edit-find-symbolic")  # create an image to place on the button
		self.searchImage = Gtk.Image.new_from_gicon(self.searchIcon, Gtk.IconSize.BUTTON)
		self.searchButton = Gtk.ToggleButton(image = self.searchImage)  # creates a button with an image
		self.searchButton.connect("clicked", self.searchButton_cb, parent)  # connects the activate signal to searchButton_cb
		self.pack_end(self.searchButton)  # adds the button to the end of the headerbar

	def randomMovieButton_cb(self, randomMovieButton):
		number_movies = len(self.db.movies) - 1
		movie_position = random.randint(0, number_movies)
		movie = self.db.movies[movie_position]

		print("Title:", movie.title)
		print("Release Date:", movie.release_date)
		print("Rating:", movie.vote)
		print("Runtime:", movie.runtime)
		print("Genres:", end = " ")
		for i in range(0, len(movie.genres)):
			print(movie.genres[i], end = " ")
		print("")
		print("Overview:", movie.overview)
		# GOing to need a try except for this,
		# get_image(movie.poster_path, movie.title)
		print('')

	# callback for when the searchButton is pressed
	def searchButton_cb(self, searchButton, parent):
		if searchButton.get_active() is True:
			parent.reveal.set_transition_type(Gtk.RevealerTransitionType.SLIDE_DOWN)
			parent.reveal.set_reveal_child(True)
			parent.searchBar.searchEntry.grab_focus()
		else:
			parent.reveal.set_transition_type(Gtk.RevealerTransitionType.SLIDE_UP)
			parent.reveal.set_reveal_child(False)
			self.grab_focus()

	def dataButton_cb(self, dataButton):
		self.dataPopover.show_all()

	def manipulateMovieButton_cb(self, movieButton, parent, action):
		manipulateDialog = MovieDialog(parent, action)

	def manipulateFriend_cb(self, friendButton, parent, action):
		manipulateDialog = FriendDialog(parent, action)
