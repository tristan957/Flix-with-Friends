import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from Window2 import Window


FLIX_APP_ID = "com.return0software.Flix-with-Friends"

class FlixApplication(Gtk.Application):
	def __init__(self):
		Gtk.Application.__init__(self, application_id = FLIX_APP_ID)

		self.appWindow = None

		self.connect("activate", self.activate_cb)

	def windowCheck(self):
		if self.appWindow == None:
			self.appWindow = Window(self)
			self.appWindow.connect("delete-event", Gtk.main_quit) # when delete-event signal is received, calls Gtk.main_quit
			self.appWindow.show_all()	 # display the window and all widgets

	def activate_cb(self, app):
		self.windowCheck()
		self.appWindow.present()
