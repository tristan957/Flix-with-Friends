import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class FileChooserBox(Gtk.Box):

    def __init__(self, win):
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL, spacing = 50)

        self.buttonBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 50)
        self.google = Gtk.Button(label = "Google Sheet")
        self.label = Gtk.Label("Choose the location of your file", use_markup = True)
        self.local = Gtk.Button(label = "Local Spreadsheet")
        self.buttonBox.add(self.google)
        self.buttonBox.add(self.local)
        self.add(self.label)
        self.add(self.buttonBox)
