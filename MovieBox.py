import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib
from Database import Database

MOVIE_INDEX = 11


class MovieBox(Gtk.Box):

    def __init__(self, movie):
        db = Database(Database.location)
        # movie = db.movies[MOVIE_INDEX]

        if movie_num is not None:
            Gtk.Box.__init__(self, orientation = Gtk.Orientation.HORIZONTAL)

            movie = db.get_movie(movie) # needs to be implemented

            imageBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 30)
            infoBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 20)

            titleLabel = Gtk.Label(label = "<big><b>" + movie.title + "</b></big>", justify = Gtk.Justification.CENTER, use_markup = True)
            poster = Gtk.Image(file = "./imagePosters/" + movie.title.replace(" ", "") + "_w342.jpg")
            viewedLabel = Gtk.Label(label = "<b>Viewed By:</b> " + ', '.join(movie.viewers).rstrip(','), justify = Gtk.Justification.LEFT, use_markup = True)
            viewedLabel.set_xalign(0)
            genreLabel = Gtk.Label(label = "<b>Genres:</b> " + ', '.join(movie.genres).rstrip(','), justify = Gtk.Justification.LEFT, use_markup = True)
            genreLabel.set_xalign(0)
            ratingLabel = Gtk.Label(label = "<b>Rating:</b> " + str(movie.vote) + "/10", justify = Gtk.Justification.LEFT, use_markup = True)
            ratingLabel.set_xalign(0)
            runtimeLabel = Gtk.Label(label = "<b>Runtime:</b> " + str(int(movie.runtime) // 60) + " Hours " + str(int(movie.runtime) % 60) + " Minutes", justify = Gtk.Justification.LEFT, use_markup = True)
            runtimeLabel.set_xalign(0)

            description = Gtk.Label(label = "<b>Description:</b> " + self.generateDescription(movie.overview), justify = Gtk.Justification.LEFT, use_markup = True)
            description.set_xalign(0)

            imageBox.add(titleLabel)
            imageBox.add(poster)

            infoBox.add(viewedLabel)
            infoBox.add(genreLabel)
            infoBox.add(ratingLabel)
            infoBox.add(runtimeLabel)
            infoBox.add(description)

            self.add(imageBox)
            self.add(infoBox)
        else:
            Gtk.Box.__init__(self, orientation = Gtk.Orientation.HORIZONTAL, halign = Gtk.Align.CENTER, valign = Gtk.Align.CENTER)
            titleLabel = Gtk.Label(label = "<big><b>Start typing or click\nthe search icon to begin a search</b></big>", justify = Gtk.Justification.CENTER, use_markup = True)
            self.add(titleLabel)

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
