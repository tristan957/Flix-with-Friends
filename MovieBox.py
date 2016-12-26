import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib
from Database import Database

class MovieBox(Gtk.Box):

    def __init__(self):
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.HORIZONTAL)

        self.imageBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 30)
        self.infoBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 20)

        self.titleLabel = Gtk.Label(label = "Iron Man", justify = Gtk.Justification.CENTER)
        self.poster = Gtk.Image(file = "./imagePosters/SavingPrivateRyan_w154.jpg")
        self.viewedLabel = Gtk.Label(label = "Viewed By: T, C, G, A, M, P", justify = Gtk.Justification.LEFT)
        self.viewedLabel.set_xalign(0)
        self.ratingLabel = Gtk.Label(label = "Rating: 8/10", justify = Gtk.Justification.LEFT)
        self.ratingLabel.set_xalign(0)
        self.description = Gtk.Label(label = "Description: A movie", justify = Gtk.Justification.LEFT)
        self.description.set_xalign(0)

        self.imageBox.add(self.titleLabel)
        self.imageBox.add(self.poster)

        self.infoBox.add(self.viewedLabel)
        self.infoBox.add(self.ratingLabel)
        self.infoBox.add(self.description)

        self.add(self.imageBox)
        self.add(self.infoBox)