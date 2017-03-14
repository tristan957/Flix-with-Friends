import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
from Database import Database
from InfoBox import InfoBox
from SearchBar import SearchBar
from HeaderBar import HeaderBar


class LocationChooser(Gtk.Box):

	def __init__(self):
		"""initial box to choose the location of the database"""
		Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL, margin = 20, spacing = 10)

		label = Gtk.Label("<big>Choose the location of your spreadsheet.</big>", use_markup = True)
		self.pack_start(label, True, True, 0)

		googleIcon = Gio.ThemedIcon(name = "google")
		googleImage = Gtk.Image.new_from_gicon(googleIcon, Gtk.IconSize.BUTTON)
		self.google = Gtk.Button(label = "Google Sheet", image = googleImage, image_position = Gtk.PositionType.LEFT, always_show_image = True)

		localIcon = Gio.ThemedIcon(name = "folder-symbolic")
		localImage = Gtk.Image.new_from_gicon(localIcon, Gtk.IconSize.BUTTON)
		self.local = Gtk.Button(label = "Local Spreadsheet", image = localImage, image_position = Gtk.PositionType.LEFT, always_show_image = True)

		buttonBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
		buttonBox.get_style_context().add_class("linked")
		buttonBox.pack_start(self.google, True, True, 0)
		buttonBox.pack_end(self.local, True, True, 0)
		buttonBox.set_size_request(500, 100)
		self.pack_end(buttonBox, False, True, 0)

class Window(Gtk.Window):

	def __init__(self):
		"""the main application window"""
		Gtk.Window.__init__(self)

		header = Gtk.HeaderBar(title = "Flix with Friends", show_close_button = True) # dummy header bar
		self.set_titlebar(header)

		self.stack = Gtk.Stack(homogeneous = True, transition_type = Gtk.StackTransitionType.SLIDE_LEFT_RIGHT) # creates the main stack

		spreadsheetBox = LocationChooser() # look up
		spreadsheetBox.google.connect("clicked", self.google_cb)
		spreadsheetBox.local.connect("clicked", self.local_cb)
		self.stack.add_named(spreadsheetBox, "data-chooser")

		label1 = Gtk.Label("Choose the location of your file", use_markup = True)
		self.stack.add_named(label1, "label")

		self.box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		self.box.pack_end(self.stack, True, True, 0)

		self.add(self.box)

		self.show_all()

	def key_pressed_cb(self, win, event):
		"""grab key presses to open the search bar"""
		self.searchBar.set_transition_type(Gtk.RevealerTransitionType.SLIDE_DOWN)
		self.searchBar.set_reveal_child(True)
		if self.searchBar.searchEntry.has_focus() is False:
			self.searchBar.searchEntry.grab_focus()
		self.header.searchButton.set_active(True)
		return self.searchBar.searchEntry.handle_event(event)

	def google_cb(self, google):
		self.stack.set_visible_child_name("label")

	def local_cb(self, local):
		"""ask the user for an excel file"""
		fileChooser = Gtk.FileChooserDialog(self, title = "Choose a Spreadsheet")
		fileFilter = Gtk.FileFilter()
		fileFilter.add_mime_type("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
		fileFilter.add_mime_type("application/vnd.ms-excel")
		fileChooser.add_filter(fileFilter)
		fileChooser.add_button("Open", Gtk.FileChooserAction.OPEN)
		fileChooser.add_button("Cancel", Gtk.ResponseType.CANCEL)
		fileChooser.set_transient_for(self)
		fileChooser.connect("file_activated", self.doubleClickEnter_cb)
		if fileChooser.run() is 0: # 0 stands for file being chosen
			# Database.location = fileChooser.get_filename()
			Database.location = 'local.xlsx' # TEMP
			self.addMainStack(Database.location)
			self.stack.set_visible_child_name("main")
		fileChooser.destroy()

	def doubleClickEnter_cb(self, fileChooser):
		"""enable double click functionality in the file chooser"""
		# Database.location = fileChooser.get_filename()
		Database.location = 'local.xlsx' # TEMP
		fileChooser.destroy()
		self.addMainStack(Database.location)
		self.stack.set_visible_child_name("main")

	def addMainStack(self, location):
		"""adds the main stack to the window"""
		box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		self.searchBar = SearchBar(location, self)
		self.box.pack_start(self.searchBar, False, False, 0)
		noneBox = InfoBox(None) # initial box after location has been chosen
		# box.add(imdbBox)
		self.stack.add_named(noneBox, "main")

		self.header = HeaderBar(self)
		self.set_titlebar(self.header)

		self.connect("key-press-event", self.key_pressed_cb)

		self.show_all()
