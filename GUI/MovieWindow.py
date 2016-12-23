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
		self.reveal = Gtk.Revealer(child = self.searchBar, transition_type = Gtk.RevealerTransitionType.SLIDE_DOWN, transition_duration = 500)
		self.add(self.reveal)
		self.connect("key-press-event", self.key_pressed_cb, self.reveal)

	def key_pressed_cb(self, win, event, reveal):
		reveal.set_reveal_child(True)
		return self.searchBar.search.handle_event(event)
