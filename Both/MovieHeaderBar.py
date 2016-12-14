import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib
from Database import Database


class MovieHeaderBar(Gtk.HeaderBar):

    def __init__(self):
        Gtk.HeaderBar.__init__(
            self, title="Stop Bitchin', Start Watchin'", show_close_button=True)

        self.fileButton = Gtk.FileChooserButton()  # create a Gtk.FileChooserButton
        # connects the file-set signal to fileButton_cb
        self.fileButton.connect("file-set", self.fileButton_cb)
        # adds the button to the start of the headerbar
        self.pack_start(self.fileButton)

        # button to display popover displaying add/delete options to data
        dataIcon = Gio.ThemedIcon(name="open-menu-symbolic")
        dataImage = Gtk.Image.new_from_gicon(dataIcon, Gtk.IconSize.BUTTON)

        self.addMovieButton = Gtk.Button(label="Add a Movie")
        self.deleteMovieButton = Gtk.Button(label="Delete a Movie")
        dataBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        dataBox.add(self.addMovieButton)
        dataBox.add(self.deleteMovieButton)
        self.dataButton = Gtk.Button(image=dataImage)
        self.dataButton.connect("clicked", self.dataButton_cb)
        self.dataPopover = Gtk.Popover(
            position=Gtk.PositionType.BOTTOM, relative_to=self.dataButton)
        self.dataPopover.add(dataBox)
        self.pack_end(self.dataButton)

        self.randomMovieButton = Gtk.Button(label="Random Movie")
        self.randomMovieButton.connect("clicked", self.randomMovieButton_cb)
        self.pack_end(self.randomMovieButton)

        # create an image to place on the button
        self.searchIcon = Gio.ThemedIcon(name="edit-find-symbolic")
        self.searchImage = Gtk.Image.new_from_gicon(
            self.searchIcon, Gtk.IconSize.BUTTON)
        # creates a button with an image
        self.searchButton = Gtk.Button(image=self.searchImage)
        # connects the activate signal to searchButton_cb
        self.searchButton.connect("clicked", self.searchButton_cb)
        # adds the button to the end of the headerbar
        self.pack_end(self.searchButton)

    # callback for when the fileButton is pressed
    def fileButton_cb(self, fileButton):
        filename = fileButton.get_filename()
        db = Database(filename)
        Database.location = filename
        db.loadDB()

    def randomMovieButton_cb(self, randomMovieButton):
        print("Random Movie")

    # callback for when the searchButton is pressed
    def searchButton_cb(self, searchButton):
        print("Search")

    def dataButton_cb(self, dataButton):
        self.dataPopover.show_all()
