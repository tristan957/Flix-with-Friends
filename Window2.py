import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio
from Database import Database

class LocationChooser(Gtk.Box):
	"""Box to choose the location of information for the database"""
	def __init__(self):
		Gtk.Box.__init__(self, margin = 100,
						orientation = Gtk.Orientation.VERTICAL, spacing = 100)

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

		# button to set up the database from a local folder
		localIcon = Gio.ThemedIcon(name = "folder-symbolic")
		localImage = Gtk.Image.new_from_gicon(localIcon, Gtk.IconSize.BUTTON)
		self.local = Gtk.Button(label = "Local Folder", image = localImage,
								image_position = Gtk.PositionType.TOP, always_show_image = True)

		# button to set up the database from a folder/server
		serverIcon = Gio.ThemedIcon(name = "network-server-symbolic")
		serverImage = Gtk.Image.new_from_gicon(serverIcon, Gtk.IconSize.BUTTON)
		self.server = Gtk.Button(label = "Server", image = serverImage,
								image_position = Gtk.PositionType.TOP, always_show_image = True)

		# button to set up the database from a local spreadsheet
		spreadsheetIcon = Gio.ThemedIcon(name = "x-office-spreadsheet")
		spreadsheetImage = Gtk.Image.new_from_gicon(spreadsheetIcon, Gtk.IconSize.BUTTON)
		self.spreadsheet = Gtk.Button(label = "Spreadsheet", image = spreadsheetImage,
								image_position = Gtk.PositionType.TOP, always_show_image = True)

		buttons.pack_start(self.google, True, True, 0)
		buttons.pack_start(self.local, True, True, 0)
		buttons.pack_start(self.server, True, True, 0)
		buttons.pack_end(self.spreadsheet, True, True, 0)

		self.pack_end(buttons, True, False, 0)

class Window(Gtk.Window):
	"""Window where all the magic happens"""
	def __init__(self):
		Gtk.Window.__init__(self)

		header = Gtk.HeaderBar(title = "Flix with Friends", show_close_button = True)
		self.set_titlebar(header)

		locationChooser = LocationChooser()
		self.add(locationChooser)
