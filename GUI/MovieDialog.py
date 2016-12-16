import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MovieDialog(Gtk.Window):

	def __init__(self, action):
		Gtk.Window.__init__(self, title = action + " a Movie")

		self.header = Gtk.HeaderBar(title = action + " a Movie", show_close_button = True)
		self.set_titlebar(self.header)

		self.box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 5)
		self.entry = Gtk.Entry()
		self.entry.grab_focus()
		self.box.add(self.entry)

		self.enterButton = Gtk.Button(label = "Enter")
		self.enterButton.connect("clicked", self.enterButton_cb)
		self.box.add(self.enterButton)

		self.add(self.box)

	def enterButton_cb(self, enterButton):
		self.destroy()
