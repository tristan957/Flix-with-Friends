import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from Database import Database


class MovieDialog(Gtk.Dialog):

	"""
	Dialog for adding and deleting movies
	"""

	__gsignals__ = {
		"movie-added": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,)), # in conjunction with change source button to change the database source
		"movie-deleted": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,)) # in conjunction with edit source button to bring up an edit screen
	}

	def __init__(self, parent, db, action):
		"""
		Create a dialog for adding and deleting movies
		"""
		Gtk.Dialog.__init__(self, action + " a Movie", parent, Gtk.DialogFlags.MODAL, use_header_bar = True)

		self.action = action.lower()

		self.area = self.get_content_area()	 # area is a Gtk.Box
		box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
		box.get_style_context().add_class("linked")

		label = Gtk.Label(label = "Enter the name of a friend to " + action.lower())
		self.area.pack_start(label, True, True, 0)

		self.entry = Gtk.Entry()
		self.entry.grab_focus()
		box.pack_start(self.entry, True, False, 0)

		self.enterButton = Gtk.Button(label = "Enter")
		self.enterButton.connect("clicked", self.enterButton_cb, db)
		box.pack_end(self.enterButton, True, False, 0)

		self.area.pack_start(box, True, False, 0)

		self.show_all()
		# if the action is deleting, create an autocompletion tree

	def enterButton_cb(self, enterButton, db):
		"""
		Reads the text entry and searches for a new movie to add
		"""
		if (self.action == 'add') and (self.entry.get_text() != 'Enter the name of a movie to add'):
			print('Movie to add:', self.entry.get_text())

			try:
				# self.db.newMovie(self.entry.get_text())
				# print(self.entry.get_text(), 'added as', self.db.movies[-1].title)
				search = db.tmdb_search(self.entry.get_text())
				print('Searh Results:\n')
				for movie in search:
					print('Title:', movie.title)
					print('Overview:', movie.overview)
					print()
			except:
				print('Error adding', self.entry.get_text())
		self.destroy()
