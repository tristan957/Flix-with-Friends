import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib, Pango

from Database import Database


class ViewedByFrame(Gtk.Frame):
	"""Frame for displaying who has seen the movie"""

	def __init__(self, movie):
		Gtk.Frame.__init__(self, label_xalign = .1)

		title = Gtk.Label(label = "<b>Viewed By</b>", use_markup = True)
		self.set_label_widget(title)

		self.viewers = Gtk.Label(label = movie.get_viewers_string(), wrap = True,
								margin_bottom = 5, margin_left = 5, margin_right = 5,
								halign = Gtk.Align.START, valign = Gtk.Align.CENTER)

		# box = Gtk.Box(margin_bottom = 5, margin_left = 3, margin_right = 3)
		# box.add(self.viewers)

		self.add(self.viewers)

	def update(self, movie):
		self.viewers.set_label(movie.get_viewers_string())


class GenreFrame(Gtk.Frame):
	"""Frame for the genres of the movies"""

	def __init__(self, movie):
		Gtk.Frame.__init__(self, label_xalign = .1)

		title = Gtk.Label(label = "<b>Genres</b>", use_markup = True)
		self.set_label_widget(title)

		self.genres = Gtk.Label(label = movie.get_genres_string(), wrap = True,
								margin_bottom = 5, margin_left = 5, margin_right = 5,
								halign = Gtk.Align.START, valign = Gtk.Align.CENTER)

		# box = Gtk.Box(margin_bottom = 5, margin_left = 3, margin_right = 3)
		# box.add(self.genres)

		self.add(self.genres)

	def update(self, movie):
		self.genres.set_label(movie.get_genres_string())


class RatingFrame(Gtk.Frame):
	"""Frame for displaying the rating of the movie"""

	def __init__(self, movie):
		Gtk.Frame.__init__(self, label_xalign = .1)

		title = Gtk.Label(label = "<b>Rating</b>", use_markup = True)
		self.set_label_widget(title)

		self.rating = Gtk.Label(label = movie.vote + "/10", wrap = True)
		self.level = Gtk.LevelBar.new_for_interval(0, 10)
		self.level.set_value(float(movie.vote))
		self.level.set_size_request(100, -1)

		box = Gtk.Box(margin_bottom = 5, margin_left = 5, margin_right = 5, spacing = 5)
		box.add(self.level)
		box.add(self.rating)

		self.add(box)

	def update(self, movie):
		self.rating.set_label(movie.vote)
		self.level.set_value(float(movie.vote))


class RuntimeFrame(Gtk.Frame):
	"""Frame for displaying the runtime of the movie"""

	def __init__(self, movie):
		Gtk.Frame.__init__(self, label_xalign = .1)

		title = Gtk.Label(label = "<b>Runtime</b>", use_markup = True)
		self.set_label_widget(title)
		self.runtime = Gtk.Label(label = str(int(movie.runtime) // 60) + " Hours " +
									str(int(movie.runtime) % 60) + " Minutes", wrap = True,
									margin_bottom = 5, margin_left = 5, margin_right = 5,
									halign = Gtk.Align.START, valign = Gtk.Align.CENTER)

		# box = Gtk.Box(margin_bottom = 5, margin_left = 3, margin_right = 3)
		# box.add(self.runtime)
		self.add(self.runtime)

	def update(self, movie):
		self.runtime.set_label(str(int(movie.runtime) // 60) + " Hours " +
								str(int(movie.runtime) % 60) + " Minutes")


class DescriptionFrame(Gtk.Frame):
	"""Frame for displaying who has seen the movie"""

	def __init__(self, movie):
		Gtk.Frame.__init__(self, label_xalign = .1)

		title = Gtk.Label(label = "<b>Description</b>", use_markup = True)
		self.set_label_widget(title)
		self.description = Gtk.Label(label = movie.overview, wrap = True, max_width_chars = 80,
									margin_bottom = 5, margin_left = 5, margin_right = 5,
									halign = Gtk.Align.START, valign = Gtk.Align.CENTER) # (temp fix if needed)

		# box = Gtk.Box(margin_bottom = 5, margin_left = 3, margin_right = 3)
		# box.add(self.description)

		self.add(self.description)

	def update(self, movie):
		self.description.set_label(movie.get_viewers_string())


class ImageBox(Gtk.Box):
	"""Create a box to display an image and movie title"""

	def __init__(self, movie):
		Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL, spacing = 20, margin = 20)

		self.title = Gtk.Label(label = movie.get_markup_title(), justify = Gtk.Justification.CENTER,
							use_markup = True)
		self.poster = Gtk.Image(file = movie.get_large_image())

		self.add(self.title)
		self.add(self.poster)

	def update(self, movie):
		self.title.set_label("<big><b>" + movie.title.replace('&', '&amp;') + "</b></big>")
		self.poster.set_from_file(self.movie.get_large_image())


class InfoBox(Gtk.Box): # implement as stack and create imdbBox when a movie is selected/random is clicked, then proceed to update
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

		imageBox = ImageBox(self.movie)
		# imageBox.get_style_context().add_class("frame")
		info = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10,
						hexpand = False, vexpand = True)
		info.get_style_context().add_class("inline-toolbar")

		self.viewFrame = ViewedByFrame(self.movie)
		self.genFrame = GenreFrame(self.movie)
		self.ratFrame = RatingFrame(self.movie)
		self.runFrame = RuntimeFrame(self.movie)
		self.descFrame = DescriptionFrame(self.movie)

		info.pack_start(self.viewFrame, False, False, 0)
		info.pack_start(self.genFrame, False, False, 0)
		info.pack_start(self.ratFrame, False, False, 0)
		info.pack_start(self.runFrame, False, False, 0)
		info.pack_start(self.descFrame, False, False, 0)

		self.pack_start(imageBox, True, True, 0)
		self.pack_end(info, False, False, 0)

		self.show_all()

	def update(self, movieName):
		self.movie = self.db.find_movie(movieName)

		self.viewFrame.update(self.movie)
		self.genFrame.update(self.movie)
		self.ratFrame.update(self.movie)
		self.runFrame.update(self.movie)
		self.descFrame.update(self.movie)

		self.queue_draw()
