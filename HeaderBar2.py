import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GObject

from FriendDialog import FriendDialog
from MovieDialog import MovieDialog


class DataButton(Gtk.MenuButton):
	"""Create a button for manipulating database data"""

	__gsignals__ = {
		"source-change": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,)), # in conjunction with change source button to change the database source
		"source-edit": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,)) # in conjunction with edit source button to bring up an edit screen
	}

	def __init__(self, win):
		Gtk.Button.__init__(self)

		self.win = win
		self.pop = None

		ADD = "Add"
		DELETE = "Delete"

		icon = Gio.ThemedIcon(name = "open-menu-symbolic")
		image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)

		change = Gtk.ModelButton(text = "Change Source")
		edit = Gtk.ModelButton(text = "Edit Source")
		addMovie = Gtk.ModelButton(text = "Add a Movie")
		deleteMovie = Gtk.ModelButton(text = "Delete a Movie")
		addFriend = Gtk.ModelButton(text = "Add a Friend")
		deleteFriend = Gtk.ModelButton(text = "Delete a Friend")

		change.connect("clicked", self.change_cb)
		edit.connect("clicked", self.edit_cb)
		addMovie.connect("clicked", self.manipulateMovies_cb, ADD)
		deleteMovie.connect("clicked", self.manipulateMovies_cb, DELETE)
		addFriend.connect("clicked", self.manipulateFriends_cb, ADD)
		deleteFriend.connect("clicked", self.manipulateFriends_cb, DELETE)

		box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		box.add(change)
		box.add(edit)
		box.add(Gtk.SeparatorMenuItem())
		box.add(addMovie)
		box.add(deleteMovie)
		box.add(Gtk.SeparatorMenuItem())
		box.add(addFriend)
		box.add(deleteFriend)

		self.pop = Gtk.PopoverMenu(position = Gtk.PositionType.BOTTOM)
		self.pop.add(box)

		self.set_image(image)
		self.set_use_popover(True)
		self.set_popover(self.pop)

	def get_pop(self):
		return self.pop

	def change_cb(self, button):
		print("This is a dummy callback for the Change Source button.")

	def edit_cb(self, button):
		print("This is a dummy callback for the Edit Source button.")

	def manipulateMovies_cb(self, movieButton, action):
		dialog = MovieDialog(self.win, action)

	def manipulateFriends_cb(self, friendButton, action):
		dialog = FriendDialog(self.win, action)

class HeaderBar(Gtk.HeaderBar):
	"""Creates a header bar for the window"""

	__gsignals__ = {
		"random-clicked": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()), # in conjunction with random movie button to facilitate a search
		"revealer-change": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,)),
		"source-change": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,)), # in conjunction with change source button to change the database source
		"source-edit": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,)) # in conjunction with edit source button to bring up an edit screen
	}

	def __init__(self, win):
		Gtk.HeaderBar.__init__(self, title = "Flix with Friends", show_close_button = True)

		self.win = win
		self.randMovie = None

		self.randMovie = Gtk.Button(label = "Random Movie")
		self.randMovie.get_style_context().add_class("suggested-action")

		data = DataButton(win)

		searchIcon = Gio.ThemedIcon(name = "edit-find-symbolic")
		searchImage = Gtk.Image.new_from_gicon(searchIcon, Gtk.IconSize.BUTTON)
		self.search = Gtk.ToggleButton(image = searchImage)

		self.randMovie.connect("clicked", self.randMovie_cb) # come back to this
		data.connect("clicked", self.data_cb)
		self.search.connect("clicked", self.search_cb)

		self.pack_start(self.randMovie)
		self.pack_end(data)
		self.pack_end(self.search)

	def data_cb(self, data):
		data.get_pop().show_all()

	def randMovie_cb(self, button):
		self.emit("random-clicked")

	def search_cb(self, button):
		self.emit("revealer-change", button.get_active())
