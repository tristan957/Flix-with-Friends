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
		self.searchBar = MovieSearchBar()
		self.add(self.searchBar)
		self.connect("key-press-event", self.key_pressed_cb)

	def key_pressed_cb(self, win, event):
		return self.searchBar.search.handle_event(event)
