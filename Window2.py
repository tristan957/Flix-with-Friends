import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GObject

from Database import Database
from HeaderBar2 import HeaderBar

class LocationChooser(Gtk.Box):
	"""Box to choose the location of information for the database"""

	__gsignals__ = {
		"location-chosen": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,))
	}

	def __init__(self, win):
		Gtk.Box.__init__(self, margin = 100,
						orientation = Gtk.Orientation.VERTICAL, spacing = 100)

		self.win = win
		self.google = None
		self.spreadsheet = None
		self.server = None
		self.local = None

		label = Gtk.Label("<big>Choose the location of your data</big>", use_markup = True)
		self.pack_start(label, True, True, 0)

		buttons = Gtk.ButtonBox(layout_style = Gtk.ButtonBoxStyle.EXPAND)
		buttons.set_size_request(500, 100)

		# button to set up the database from a Google Sheet
		googleIcon = Gio.ThemedIcon(name = "google")
		googleImage = Gtk.Image.new_from_gicon(googleIcon, Gtk.IconSize.BUTTON)
		self.google = Gtk.Button(label = "Google Sheet", image = googleImage,
								image_position = Gtk.PositionType.TOP, always_show_image = True)
		self.google.connect("clicked", self.google_cb)

		# button to set up the database from a local folder
		localIcon = Gio.ThemedIcon(name = "folder-symbolic")
		localImage = Gtk.Image.new_from_gicon(localIcon, Gtk.IconSize.BUTTON)
		self.local = Gtk.Button(label = "Local Folder", image = localImage,
								image_position = Gtk.PositionType.TOP, always_show_image = True)
		self.local.connect("clicked", self.local_cb)

		# button to set up the database from a server
		serverIcon = Gio.ThemedIcon(name = "network-server-symbolic")
		serverImage = Gtk.Image.new_from_gicon(serverIcon, Gtk.IconSize.BUTTON)
		self.server = Gtk.Button(label = "Server", image = serverImage,
								image_position = Gtk.PositionType.TOP, always_show_image = True)
		self.server.connect("clicked", self.server_cb)

		# button to set up the database from a local spreadsheet
		spreadsheetIcon = Gio.ThemedIcon(name = "x-office-spreadsheet")
		spreadsheetImage = Gtk.Image.new_from_gicon(spreadsheetIcon, Gtk.IconSize.BUTTON)
		self.spreadsheet = Gtk.Button(label = "Spreadsheet", image = spreadsheetImage,
									image_position = Gtk.PositionType.TOP, always_show_image = True)
		self.spreadsheet.connect("clicked", self.spreadsheet_cb)

		buttons.pack_start(self.google, True, True, 0)
		buttons.pack_start(self.local, True, True, 0)
		buttons.pack_start(self.server, True, True, 0)
		buttons.pack_end(self.spreadsheet, True, True, 0)

		self.pack_end(buttons, True, False, 0)

	def google_cb(self, button):
		print("This is a dummy google_cb")

	def local_cb(self, button):
		print("This is a dummy local_cb")

	def server_cb(self, button):
		print("This is a dummy server_cb")

	def spreadsheet_cb(self, button):
		"""ask the user for a spreadsheet file, more specifically a .xls/.xlsx file"""
		fileChooser = Gtk.FileChooserDialog(self.win, title = "Choose a spreadsheet")
		fileFilter = Gtk.FileFilter() # filters the file chooser
		fileFilter.add_mime_type("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet") # .xlsx
		fileFilter.add_mime_type("application/vnd.ms-excel") # .xls
		fileChooser.add_filter(fileFilter)
		fileChooser.add_button("Open", Gtk.FileChooserAction.OPEN)
		fileChooser.add_button("Cancel", Gtk.ResponseType.CANCEL)
		fileChooser.set_transient_for(self.win)
		fileChooser.connect("file_activated", self.doubleClickEnter_cb)

		if fileChooser.run() == 0: # 0 stands for file being chosen
			location = fileChooser.get_filename()
			self.emit("location-chosen", location)
		fileChooser.destroy()

	def doubleClickEnter_cb(self, fileChooser):
		"""runs if the user hits enter or double clicks an item"""
		location = fileChooser.get_filename()
		self.emit("location-chosen", location)
		fileChooser.destroy()


class InitWindow(Gtk.Window):
	"""Gets the initial location information"""

	__gsignals__ = {
		"location-chosen": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,))
	}

	def __init__(self):
		Gtk.Window.__init__(self)

		header = Gtk.HeaderBar(title = "Flix with Friends", show_close_button = True)
		self.set_titlebar(header)

		locationChooser = LocationChooser(self)
		locationChooser.connect("location-chosen", self.locationChosen_cb)

		self.add(locationChooser)

	def locationChosen_cb(self, box, location):
		self.emit("location-chosen", location)

class MainWindow(Gtk.ApplicationWindow): # window is currently acting too much like an application. use windows as windows, not as managers
	"""Window where all the magic happens"""
	def __init__(self, db):
		Gtk.Window.__init__(self)

		self.db = db
		self.windowStack = None
		self.headerBar = None
		self.searchBar = None

		self.headerBar = HeaderBar(self)
		self.set_titlebar(self.headerBar)
		self.windowStack = Gtk.Stack(interpolate_size = True,
									transition_type = Gtk.StackTransitionType.OVER_LEFT_RIGHT)
		self.add(self.windowStack)

		locationChooser = LocationChooser(self)
		# locationChooser.connect("location-chosen", self.updateWin)

		self.windowStack.add_named(locationChooser, "location-chooser")

	def updateSource(self, locationChooser, location):
		# Database.location = location
		self.show_all()
