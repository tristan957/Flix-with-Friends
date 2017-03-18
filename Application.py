import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from Database import Database
from Window2 import InitWindow, MainWindow


FLIX_APP_ID = "com.return0software.Flix-with-Friends"

class FlixApplication(Gtk.Application):
	"""acts a program manager"""
	def __init__(self):
		Gtk.Application.__init__(self, application_id = FLIX_APP_ID)

		self.appWindow = None
		self.db = None

		self.connect("activate", self.activate_cb)

	def windowCheck(self):
		"""checks if a window is already in use"""
		if self.appWindow == None:
			self.appWindow = InitWindow() # create the initial window to get a location
			self.appWindow.connect("location-chosen", self.createMainWin)
			self.add_window(self.appWindow)
			# self.appWindow.connect("delete-event", Gtk.main_quit) # when delete-event signal is received, calls Gtk.main_quit

	def activate_cb(self, app):
		"""starts the program"""
		self.windowCheck()
		self.appWindow.present()
		self.appWindow.show_all() # display the window and all widgets

	def createMainWin(self, win, location):
		"""creates the main window"""
		Database.location = location
		self.db = Database(Database.location) # create the database of the given location

		self.remove_window(self.appWindow)
		self.appWindow.destroy()
		self.appWindow = MainWindow(self.db) # create the main window now that we have an initial location
		self.appWindow.connect("delete-event", Gtk.main_quit) # when delete-event signal is received, calls Gtk.main_quit
		self.appWindow.present()
		self.appWindow.show_all()
