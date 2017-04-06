import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib

from Database import Database


class MainInfoContainer(Gtk.Box):
	"""Box to display info neatly"""

	def __init__(self, movie):
		Gtk.Box.__init__(self, margin = 20, spacing = 20)


class InfoPage(Gtk.Box):
	"""Create a single page Notebook to display movie information"""

	def __init__(self, db, movieName):
		Gtk.Box.__init__(self)

		self.db = db

		self.movie = db.find_movie(movieName)

		self.action = Gtk.ActionBar()

		self.title = Gtk.Label(label = self.movie.get_markup_title(), justify = Gtk.Justification.CENTER,
							use_markup = True)
		self.action.set_center_widget(self.title)

		self.popout = Gtk.Button(label = "Popout")
		# popout.connect("clicked", self.popout_cb)
		self.action.pack_start(self.popout)

		self.pack_start(self.action, False, False, 0)

	def update(self, movieName):
		self.movie = self.db.find_movie(movieName)

		self.title.set_label(self.movie.get_markup_title())

		# self.title.set_label(self.movie.get_markup_title())
