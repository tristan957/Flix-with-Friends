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
		# self.box = Gtk.Box(spacing=6)
		# self.add(self.box)
		#
		# self.button1 = Gtk.Button(label="Hello")
		# #self.button1.connect("clicked", self.on_button1_clicked)
		# self.box.pack_start(self.button1, True, True, 0)
		#
		# self.button2 = Gtk.Entry()
		# self.box.pack_start(self.button2, True, True, 0)
