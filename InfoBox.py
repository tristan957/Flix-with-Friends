import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib
from Database import Database


class InfoBox(Gtk.Box):

    def __init__(self, movie_name):
        """Create a box to display relevant movie information"""
        self.db = Database(Database.location)
        # movie = db.movies[MOVIE_INDEX]

        Gtk.Box.__init__(self, orientation = Gtk.Orientation.HORIZONTAL)
        self.get_style_context().add_class("linked")

        self.movie = self.db.find_movie(movie_name)

        imageBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 20, margin = 20)
        imageBox.set_size_request(400, -1)
        # imageBox.get_style_context().add_class("frame")
        info = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 20)
        info.set_size_request(300, -1)
        info.get_style_context().add_class("inline-toolbar")

        self.titleLabel = Gtk.Label(label = "<big><b>" + self.movie.title.replace('&', '&amp;') + "</b></big>", justify = Gtk.Justification.CENTER, use_markup = True)
        self.poster = Gtk.Image(file = "./imagePosters/" + self.movie.title.replace(" ", "") + "_w342.jpg")

        viewedByTitle = Gtk.Label(label = "<b>Viewed By</b>", use_markup = True)
        self.viewers = Gtk.Label(label = ', '.join(self.movie.viewers).rstrip(','), wrap = True)
        viewedByFrame = Gtk.Frame(label_widget = viewedByTitle, label_xalign = .1)
        viewedByBox = Gtk.Box(margin_bottom = 5, margin_left = 3, margin_right = 3)
        viewedByBox.add(self.viewers)
        viewedByFrame.add(viewedByBox)

        genreTitle = Gtk.Label(label = "<b>Genres</b>", use_markup = True)
        self.genres = Gtk.Label(label = ', '.join(self.movie.genres).rstrip(','), wrap = True)
        genreFrame = Gtk.Frame(label_widget = genreTitle, label_xalign = .1)
        genreBox = Gtk.Box(margin_bottom = 5, margin_left = 3, margin_right = 3)
        genreBox.add(self.genres)
        genreFrame.add(genreBox)

        ratingTitle = Gtk.Label(label = "<b>Rating</b>", use_markup = True)
        self.rating = Gtk.Label(label = self.movie.vote + "/10", wrap = True)
        self.level = Gtk.LevelBar(value = 5).new_for_interval(0, 10)
        self.level.set_size_request(100, -1)
        ratingFrame = Gtk.Frame(label_widget = ratingTitle, label_xalign = .1)
        ratingBox = Gtk.Box(margin_bottom = 5, margin_left = 3, margin_right = 3, spacing = 5)
        ratingBox.add(self.level)
        ratingBox.add(self.rating)
        ratingFrame.add(ratingBox)

        runtimeTitle = Gtk.Label(label = "<b>Runtime</b>", use_markup = True)
        self.runtime = Gtk.Label(label = str(int(self.movie.runtime) // 60) + " Hours " + str(int(self.movie.runtime) % 60) + " Minutes", wrap = True)
        runtimeFrame = Gtk.Frame(label_widget = runtimeTitle, label_xalign = .1)
        runtimeBox = Gtk.Box(margin_bottom = 5, margin_left = 3, margin_right = 3)
        runtimeBox.add(self.runtime)
        runtimeFrame.add(runtimeBox)

        descriptionTitle = Gtk.Label(label = "<b>Description</b>", justify = Gtk.Justification.LEFT, use_markup = True)
        self.description = Gtk.Label(label = self.movie.overview, wrap = True)
        descriptionFrame = Gtk.Frame(label_widget = descriptionTitle, label_xalign = .1)
        descriptionBox = Gtk.Box(margin_bottom = 5, margin_left = 3, margin_right = 3)
        descriptionBox.add(self.description)
        descriptionFrame.add(descriptionBox)

        imageBox.add(self.titleLabel)
        imageBox.add(self.poster)

        info.add(viewedByFrame)
        info.add(genreFrame)
        info.add(ratingFrame)
        info.add(runtimeFrame)
        info.add(descriptionFrame)

        # info.get_style_context().add_class("list")
        # Try using a gtk.frame and a class style context of inline-toolbar for every subsection and we'll see how it goes (toolbar, frame, rubberband)
        # self.get_style_context().add_class("inline-toolbar")

        self.pack_start(imageBox, True, True, 0)
        self.pack_end(info, True, True, 0)

    def update(self, movie_name):
        """Update the box to show new information"""
        self.movie = self.db.find_movie(movie_name)
        self.titleLabel.set_label("<big><b>" + self.movie.title.replace('&', '&amp;') + "</b></big>")
        self.viewers.set_label(', '.join(self.movie.viewers).rstrip(','))
        self.genres.set_label(', '.join(self.movie.genres).rstrip(','))
        self.rating.set_label(self.movie.vote + "/10")
        self.level.set_value(float(self.movie.vote))
        self.runtime.set_label(str(int(self.movie.runtime) // 60) + " Hours " + str(int(self.movie.runtime) % 60) + " Minutes" )
        self.description.set_label(self.movie.overview)
        self.poster.set_from_file("./imagePosters/" + self.movie.title.replace(" ", "") + "_w342.jpg")
        self.queue_draw()
