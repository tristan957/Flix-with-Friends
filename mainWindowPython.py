import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class movieWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title = "Stop Bitchin', Start Watchin'")

		header = Gtk.HeaderBar()
		header.set_show_close_button(True)
		header.props.title = "Stop Bitchin', Start Watchin'"

		fileButton = Gtk.FileChooserButton()
		fileButton.connect("file-set", self.fileButton_cb)
		header.pack_start(fileButton)
		self.set_titlebar(header)

	def fileButton_cb(self, fileButton):
		filename = fileButton.get_filename()
		print(filename)

win = movieWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
