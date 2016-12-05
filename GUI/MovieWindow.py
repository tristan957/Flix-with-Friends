import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from ProgramHeaderBar import ProgramHeaderBar

class MovieWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title = "Stop Bitchin', Start Watchin'")

		header = ProgramHeaderBar()	#create header
		self.set_titlebar(header)	#add it to the window
