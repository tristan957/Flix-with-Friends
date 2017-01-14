import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from Database import Database


class MovieDialog(Gtk.Dialog):

	def __init__(self, parent, action):
		Gtk.Dialog.__init__(self, action + " a Movie", parent, Gtk.DialogFlags.MODAL, use_header_bar = True)

		self.db = Database(Database.location)

		self.type = action.lower()
		self.area = self.get_content_area()	 # area is a Gtk.Box
		self.area.set_orientation(Gtk.Orientation.HORIZONTAL)
		self.area.set_spacing(5)

		self.entry = Gtk.Entry(text = "Enter the name of a movie to " + action.lower())
		self.entry.grab_focus()
		self.area.add(self.entry)

		self.enterButton = Gtk.Button(label = "Enter")
		self.enterButton.connect("clicked", self.enterButton_cb)
		self.area.add(self.enterButton)

		self.show_all()
		# if the action is deleting, create an autocompletion tree

	def enterButton_cb(self, enterButton):
		if (self.type == 'add') and (self.entry.get_text() != 'Enter the name of a movie to add'):
			print('Movie to add:', self.entry.get_text())

			try:
				self.db.newMovie(self.entry.get_text())
				print(self.entry.get_text(),'added as', self.db.movies[-1].title)
			except:
				print('Error adding', self.entry.get_text())

		self.destroy()
