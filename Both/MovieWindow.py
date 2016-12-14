import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from MovieHeaderBar import MovieHeaderBar
from MovieSearchBar import MovieSearchBar

class MovieWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title = "Stop Bitchin', Start Watchin'")

		header = MovieHeaderBar()	#create headerbar
		self.set_titlebar(header)	#add it to the window
		self.search = MovieSearchBar()
		self.add(self.search)
