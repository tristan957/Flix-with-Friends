import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MovieDialog(Gtk.Dialog):

	def __init__(self, parent, action):
		Gtk.Dialog.__init__(self, action + " a Movie", parent, Gtk.DialogFlags.MODAL, use_header_bar = True)

		self.area = self.get_content_area()	#area is a Gtk.Box
		self.area.set_orientation(Gtk.Orientation.HORIZONTAL)
		self.area.set_spacing(5)

		self.entry = Gtk.Entry(text = "Enter the name of a movie to " + action.lower())
		self.entry.grab_focus()
		self.area.add(self.entry)

		self.enterButton = Gtk.Button(label = "Enter")
		self.enterButton.connect("clicked", self.enterButton_cb)
		self.area.add(self.enterButton)

		self.show_all()
		#if the action is deleting, create an autocompletion tree

	def enterButton_cb(self, enterButton):
		self.destroy()
