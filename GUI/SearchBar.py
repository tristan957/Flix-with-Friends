import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class SearchBar(Gtk.Box):
	#needs a grid of GtkToggleButtons
	def __init__(self, win):
		Gtk.Box.__init__(Gtk.Orientation.VERTICAL, spacing = 100)

		#self.entry = Gtk.SearchEntry()
		#self.set_halign(Gtk.Align.START)
