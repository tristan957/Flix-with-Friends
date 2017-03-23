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

        title = Gtk.Label(label = "<b>Genres</b>", use_markup = True)
        self.set_label_widget(title)

		self.genres = Gtk.Label(label = movie.get_genres_string(), wrap = True)

		box = Gtk.Box(margin_bottom = 5, margin_left = 3, margin_right = 3)
		box.add(self.genres)

        self.add(genreBox)

    def update(self, movie):
        self.genres.set_label(movie.get_genres_string())


class RatingFrame(Gtk.Frame):
    """Frame for displaying the rating of the movie"""

    def __init__(self, movie):
        Gtk.Frame(self, label_xalign = .1)

        title = Gtk.Label(label = "<b>Rating</b>", use_markup = True)
        self.set_label_widget(title)

        self.rating = Gtk.Label(label = movie.vote + "/10", wrap = True)
		self.level = Gtk.LevelBar(value = float(self.movie.vote)).new_for_interval(0, 10)
		self.level.set_size_request(100, -1)

		box = Gtk.Box(margin_bottom = 5, margin_left = 3, margin_right = 3, spacing = 5)
		box.add(self.level)
	    box.add(self.rating)

		self.add(ratingBox)

    def update(self, movie):
        self.rating.set_label(movie.vote)
        self.level.set_value(float(movie.vote))


class RuntimeFrame(Gtk.Frame):
    """Frame for displaying the runtime of the movie"""

    def __init__(self, movie):
        Gtk.Frame(self, label_xalign = .1)

        title = Gtk.Label(label = "<b>Runtime</b>", use_markup = True)
        self.set_label_widget(title)
		self.runtime = Gtk.Label(label = str(int(movie.runtime) // 60) + " Hours " +
                                    str(int(movie.runtime) % 60) + " Minutes", wrap = True)

		box = Gtk.Box(margin_bottom = 5, margin_left = 3, margin_right = 3)
		box.add(self.runtime)
		self.add(box)

    def update(self, movie):
        self.runtime.set_label(str(int(movie.runtime) // 60) + " Hours " +
                                str(int(movie.runtime) % 60) + " Minutes")


class DescriptionFrame(Gtk.Frame):
    """Frame for displaying who has seen the movie"""

    def __init__(self, movie):
        Gtk.Frame(self, label_xalign = .1)

        title = Gtk.Label(label = "<b>Description</b>", justify = Gtk.Justification.LEFT,
                            use_markup = True)
        self.set_label_widget(title)
		self.description = Gtk.Label(label = movie.overview, wrap = True)

		box = Gtk.Box(margin_bottom = 5, margin_left = 3, margin_right = 3)
		box.add(self.description)

		self.add(box)

    def update(self, movie):
        self.description.set_label(movie.get_viewers_string())


class ImageBox(Gtk.Box):
    """Create a box to display an image and movie title"""

    def __init__(self, movie):
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL, spacing = 20, margin = 20)

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
        self.viewFrame = None
        self.genFrame = None
        self.ratFrame = None
        self.runFrame = None
        self.descFrame = None

        self.get_style_context().add_class("linked")

        self.movie = db.find_movie(movieName)

    def update(self, movieName):
        self.movie = db.find_movie(movieName)
