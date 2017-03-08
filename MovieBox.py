import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib
from Database import Database

MOVIE_INDEX = 11

# class NoneBox():
    # Gtk.Box.__init__(self, orientation = Gtk.Orientation.HORIZONTAL, halign = Gtk.Align.CENTER, valign = Gtk.Align.CENTER)
    # titleLabel = Gtk.Label(label = "<big><b>Start typing or click\nthe search icon to begin a search</b></big>", justify = Gtk.Justification.CENTER, use_markup = True)
    # self.add(titleLabel)

class MovieBox(Gtk.Box):

    def __init__(self, movie_name):
        self.db = Database(Database.location)
        # movie = db.movies[MOVIE_INDEX]

        Gtk.Box.__init__(self, orientation = Gtk.Orientation.HORIZONTAL)

        self.movie = self.db.find_movie(movie_name)

        if self.movie is None:
            self.movie = self.db.movies[0]
        imageBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 30)
        infoBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 20)

        self.titleLabel = Gtk.Label(label = "<big><b>" + self.movie.title + "</b></big>", justify = Gtk.Justification.CENTER, use_markup = True)
        self.poster = Gtk.Image(file = "./imagePosters/" + self.movie.title.replace(" ", "") + "_w342.jpg")
        self.viewedLabel = Gtk.Label(label = "<b>Viewed By:</b> " + ', '.join(self.movie.viewers).rstrip(','), justify = Gtk.Justification.LEFT, use_markup = True)
        self.viewedLabel.set_xalign(0)
        self.genreLabel = Gtk.Label(label = "<b>Genres:</b> " + ', '.join(self.movie.genres).rstrip(','), justify = Gtk.Justification.LEFT, use_markup = True)
        self.genreLabel.set_xalign(0)
        self.ratingLabel = Gtk.Label(label = "<b>Rating:</b> " + str(self.movie.vote) + "/10", justify = Gtk.Justification.LEFT, use_markup = True)
        self.ratingLabel.set_xalign(0)
        self.runtimeLabel = Gtk.Label(label = "<b>Runtime:</b> " + str(int(self.movie.runtime) // 60) + " Hours " + str(int(self.movie.runtime) % 60) + " Minutes", justify = Gtk.Justification.LEFT, use_markup = True)
        self.runtimeLabel.set_xalign(0)

        self.description = Gtk.Label(label = "<b>Description:</b> " + self.generateDescription(self.movie.overview), justify = Gtk.Justification.LEFT, use_markup = True)
        self.description.set_xalign(0)

        imageBox.add(self.titleLabel)
        imageBox.add(self.poster)

        infoBox.add(self.viewedLabel)
        infoBox.add(self.genreLabel)
        infoBox.add(self.ratingLabel)
        infoBox.add(self.runtimeLabel)
        infoBox.add(self.description)

        self.add(imageBox)
        self.add(infoBox)

    def update(self, movie_name):
        self.movie = self.db.find_movie(movie_name)
        self.titleLabel.set_label("<big><b>" + self.movie.title + "</b></big>")
        self.viewedLabel.set_label("<b>Viewed By:</b> " + ', '.join(self.movie.viewers).rstrip(','))
        self.genreLabel.set_label("<b>Genres:</b> " + ', '.join(self.movie.genres).rstrip(','))
        self.ratingLabel.set_label("<b>Rating:</b> " + str(self.movie.vote) + "/10")
        self.runtimeLabel.set_label("<b>Runtime:</b> " + str(int(self.movie.runtime) // 60) + " Hours " + str(int(self.movie.runtime) % 60) + " Minutes" )
        self.description.set_label("<b>Description:</b> " + self.generateDescription(self.movie.overview))
        self.poster.set_from_file("./imagePosters/" + self.movie.title.replace(" ", "") + "_w342.jpg")
        self.show_all()

    def generateDescription(self, descriptionText):
        CHARACTERS_IN_LINE = 50  # Numbers of chars before inserting \n
        TAB = 18 * ' '
        i = len(TAB)
        FLAG = True
        while i < len(descriptionText):
            i += 1
            if (i % CHARACTERS_IN_LINE) == 0:
                if FLAG:
                    i -= len(TAB)
                    FLAG = False
                while descriptionText[i] != ' ':
                    if i < len(descriptionText) - 1:
                        i += 1
                    else:
                        break
                descriptionText = descriptionText[:i] + '\n' + TAB + descriptionText[i:]
                i += len(TAB)
                FLAG = True

        return descriptionText
