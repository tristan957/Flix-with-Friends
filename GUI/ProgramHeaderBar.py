import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio

class ProgramHeaderBar(Gtk.HeaderBar):

	def __init__(self):
		Gtk.HeaderBar.__init__(self, title = "Stop Bitchin', Start Watchin'", show_close_button = True)

		self.fileButton = Gtk.FileChooserButton()	#create a Gtk.FileChooserButton
		self.fileButton.connect("file-set", self.fileButton_cb)	#connects the file-set signal to fileButton_cb
		self.pack_start(self.fileButton)	#adds the button to the start of the headerbar

		self.searchImage = Gtk.Image(stock = Gtk.STOCK_FIND)	#create an image to place on the button
		self.searchButton = Gtk.Button(image = self.searchImage)	#creates a button with an image
		self.searchButton.connect("activate", self.searchButton_cb)	#connects the activate signal to searchButton_cb
		self.pack_end(self.searchButton)	#adds the button to the end of the headerbar

	#callback for when the fileButton is pressed
	def fileButton_cb(self, fileButton):
		filename = fileButton.get_filename()

	#callback for when the searchButton is pressed
	def searchButton_cb(self, searchButton):
		print("search")
