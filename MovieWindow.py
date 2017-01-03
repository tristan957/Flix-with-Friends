import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from MovieHeaderBar import MovieHeaderBar
from MovieSearchBar import MovieSearchBar
from MovieBox import MovieBox

class MovieWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title = "Flix with Friends")

		self.box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		self.searchBar = MovieSearchBar()
		self.reveal = Gtk.Revealer(child = self.searchBar, transition_duration = 500)
		self.box.add(self.reveal)
		self.imdbBox = MovieBox()
		self.box.add(self.imdbBox)
		self.add(self.box)
		self.header = MovieHeaderBar(self, self.reveal, self.searchBar)	#create headerbar
		self.set_titlebar(self.header)	#add it to the window
		self.connect("key-press-event", self.key_pressed_cb, self.reveal, self.searchBar, self.header)

	def key_pressed_cb(self, win, event, reveal, searchBar, header):
		reveal.set_transition_type(Gtk.RevealerTransitionType.SLIDE_DOWN)
		header.searchButton.set_active(True)
		reveal.set_reveal_child(True)
		return self.searchBar.search.handle_event(event)
