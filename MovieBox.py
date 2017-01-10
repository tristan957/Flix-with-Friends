import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib
from Database import Database

MOVIE_INDEX = 58


class MovieBox(Gtk.Box):

    def __init__(self):
        db = Database(Database.location)
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.HORIZONTAL)

        self.imageBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 30)
        self.infoBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 20)

        self.titleLabel = Gtk.Label(label = "<big><b>" + db.movies[MOVIE_INDEX].title + "</b></big>", justify = Gtk.Justification.CENTER, use_markup = True)
        self.poster = Gtk.Image(file = "./imagePosters/" + db.movies[MOVIE_INDEX].title.replace(" ", "") + "_w342.jpg")
        self.viewedLabel = Gtk.Label(label = "<b>Viewed By:</b> T, C, G, A, M, P", justify = Gtk.Justification.LEFT, use_markup = True)
        self.viewedLabel.set_xalign(0)
        self.ratingLabel = Gtk.Label(label = "<b>Rating:</b> " + str(db.movies[MOVIE_INDEX].vote) + "/10", justify = Gtk.Justification.LEFT, use_markup = True)
        self.ratingLabel.set_xalign(0)
        self.runtimeLabel = Gtk.Label(label = "<b>Runtime:</b> " + str(db.movies[MOVIE_INDEX].runtime // 60)
                                                          + " Hours "+ str(db.movies[MOVIE_INDEX].runtime % 60)
                                                          + " Minutes", justify = Gtk.Justification.LEFT, use_markup = True)
        self.runtimeLabel.set_xalign(0)

        # Generate description
        descriptionText = db.movies[MOVIE_INDEX].overview
        for i in enumerate(db.movies[MOVIE_INDEX].overview):
            if (i[0] % 35) == 0:
                descriptionText = descriptionText[:i[0]] + '\n' + descriptionText[i[0]:]

        self.description = Gtk.Label(label = "<b>Description:</b> " + descriptionText, justify = Gtk.Justification.LEFT, use_markup = True)
        self.description.set_xalign(0)

        self.imageBox.add(self.titleLabel)
        self.imageBox.add(self.poster)

        self.infoBox.add(self.viewedLabel)
        self.infoBox.add(self.ratingLabel)
        self.infoBox.add(self.runtimeLabel)
        self.infoBox.add(self.description)

        self.add(self.imageBox)
        self.add(self.infoBox)
