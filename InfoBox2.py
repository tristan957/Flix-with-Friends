import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib

from Database import Database


class ViewedByFrame(Gtk.Frame):
    """Frame for displaying who has seen the movie"""

    def __init__(self, movie):
        Gtk.Frame(self, label_xalign = .1)

        self.viewers = Gtk.Label(label = movie.get_viewers_string(), wrap = True)

        title = Gtk.Label(label = "<b>Viewed By</b>", use_markup = True)
        self.set_label_widget(title)

		box = Gtk.Box(margin_bottom = 5, margin_left = 3, margin_right = 3)
		box.add(self.viewers)

        self.add(box)

    def update(self, movie):
        self.viewers.set_label(movie.get_viewers_string())


class GenreFrame(Gtk.Frame):
    """Frame for the genres of the movies"""

    def __init__(self, movie):
        Gtk.Frame(self, label_xalign = .1)


class RatingFrame(Gtk.Frame):
    """Frame for displaying the rating of the movie"""

    def __init__(self, movie):
        Gtk.Frame(self, label_xalign = .1)


class RuntimeFrame(Gtk.Frame):
    """Frame for displaying the runtime of the movie"""

    def __init__(self, movie):
        Gtk.Frame(self, label_xalign = .1)


class DescriptionFrame(Gtk.Frame):
    """Frame for displaying who has seen the movie"""

    def __init__(self, movie):
        Gtk.Frame(self, label_xalign = .1)


class ImageBox(Gtk.Box):
    """Create a box to display an image and movie title"""

    def __init__(self, movie):
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL, spacing = 20, margin = 20)

        self.set_size_request(400, -1)

        self.title = Gtk.Label(label = movie.get_markup_title(), justify = Gtk.Justification.CENTER,
                            use_markup = True)
        self.poster = Gtk.Image(file = movie.get_large_image())

        self.add(title)
        self.add(poster)

    def update(self, movie):
        self.title.set_label("<big><b>" + movie.title.replace('&', '&amp;') + "</b></big>")
        self.poster.set_from_file(self.movie.get_large_image())


class InfoBox(Gtk.Box):
    """Create a box to display relevant movie information"""

    def __init__(self, db, movieName):
        Gtk.Box.__init__(self)

        self.db = db

        self.get_style_context().add_class("linked")

        self.movie = db.find_movie(movieName)

    def update(self, movieName):
        self.movie = db.find_movie(movieName)
