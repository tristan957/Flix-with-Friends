import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib

from Database import Database


class ActBar(Gtk.ActionBar):
	"""Provides a titlebar with actions for movies"""

	def __init__(self, movie):
		Gtk.ActionBar.__init__(self)

		self.get_style_context().add_class("inline-toolbar")

		self.title = Gtk.Label(label = movie.get_markup_title(), justify = Gtk.Justification.CENTER,
								use_markup = True)
		self.set_center_widget(self.title)

		# add a button to create a dialog that contains the movie info
		pageIcon = Gio.ThemedIcon(name = "view-paged-symbolic")
		popImage = Gtk.Image.new_from_gicon(pageIcon, Gtk.IconSize.BUTTON)
		popout = Gtk.Button(image = popImage)
		# popout.connect("clicked", self.popout_cb)

		# add a button that has actions for the movie, like view trailer, view tmdb url for movie, and maybe an edit button??
		menuIcon = Gio.ThemedIcon(name = "open-menu-symbolic")
		menuImage = Gtk.Image.new_from_gicon(menuIcon, Gtk.IconSize.BUTTON)
		menu = Gtk.MenuButton(image = menuImage)

		# add a button to show a popover for who has seen the movie
		self.pop = Gtk.Popover(position = Gtk.PositionType.BOTTOM)
		self.popBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, margin = 5, spacing = 10)
		if len(movie.viewers) > 0:
			for friend in movie.viewers:
				self.popBox.add(Gtk.Label(label = friend))
		else:
			self.popBox.add(Gtk.Label(label = "No one has seen this movie."))
		self.pop.add(self.popBox)
		viewers = Gtk.MenuButton(label = "Viewers", use_popover = True, popover = self.pop)
		viewers.connect("toggled", self.viewers_cb)

		# add widgets to the ActionBar
		self.pack_start(popout)
		self.pack_end(menu)
		self.pack_end(viewers)

	def viewers_cb(self, button):
		"""Toggles the popover"""

		self.pop.show_all()

	def update(self, movie):
		"""Updates the data in the action bar"""

		self.title.set_label(movie.get_markup_title())

		# remake the popover box with new labels
		self.popBox.destroy()
		self.popBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, margin = 5, spacing = 10)
		if len(movie.viewers) > 0: # movies with no viewers for some reason have 1 viewer like "Aloha"
			for friend in movie.viewers:
				self.popBox.add(Gtk.Label(label = friend))
		else:
			self.popBox.add(Gtk.Label(label = "No one has seen this movie."))
		self.pop.add(self.popBox)

class DetailsGrid(Gtk.Grid):
	"""Create a container to display information in an organized fashion"""

	def __init__(self, movie):
		Gtk.Grid.__init__(self, column_spacing = 20, row_spacing = 10)

		self.ratingLabel = Gtk.Label(label = "<big>" + str(float(movie.vote) * 10) + "%</big>",
										use_markup = True)

		self.ratingBar = Gtk.LevelBar.new_for_interval(0, 10)
		self.ratingBar.set_inverted(True)
		self.ratingBar.set_orientation(Gtk.Orientation.VERTICAL)
		self.ratingBar.set_value(float(movie.vote))

		dateTitle = Gtk.Label(label = "<big><b>Release Date</b></big>", use_markup = True,
								halign = Gtk.Align.START)
		self.date = Gtk.Label(label = "<big>" + movie.release_date + "</big>",
								use_markup = True, halign = Gtk.Align.START)

		runtimeTitle = Gtk.Label(label = "<big><b>Runtime</b></big>", use_markup = True,
									halign = Gtk.Align.START)
		self.runtime = Gtk.Label(label = "<big>" +  str(int(movie.runtime) // 60) + " Hours " +
									str(int(movie.runtime) % 60) + " Minutes</big>", use_markup = True,
									halign = Gtk.Align.START)

		genreTitle = Gtk.Label(label = "<big><b>Genres</b></big>", use_markup = True,
								halign = Gtk.Align.START)
		self.genres = Gtk.Label(label = "<big>" + movie.get_genres_string() + "</big>",
								use_markup = True, halign = Gtk.Align.START, wrap = True,
								max_width_chars = 55) # add a wrap

		overviewTitle = Gtk.Label(label = "<big><b>Overview</b></big>", use_markup = True,
									halign = Gtk.Align.START)
		self.overview = Gtk.Label(label = "<big>" + movie.overview + "</big>", use_markup = True,
									halign = Gtk.Align.START, wrap = True, margin = 10)
		overviewScroll = Gtk.ScrolledWindow(shadow_type = Gtk.ShadowType.ETCHED_OUT, min_content_height = 200,
											min_content_width = 300, window_placement = Gtk.CornerType.TOP_LEFT)
		overviewScroll.add(self.overview)

		self.attach(self.ratingLabel, 0, 0, 1, 1)
		self.attach(self.ratingBar, 0, 1, 1, 3)
		self.attach(dateTitle, 1, 0, 1, 1)
		self.attach(self.date, 2, 0, 1, 1)
		self.attach(runtimeTitle, 1, 1, 1, 1)
		self.attach(self.runtime, 2, 1, 1, 1)
		self.attach(genreTitle, 1, 2, 1, 1)
		self.attach(self.genres, 2, 2, 1, 1)
		self.attach(overviewTitle, 1, 3, 1, 1)
		self.attach(overviewScroll, 2, 3, 1, 1)

	def update(self, movie):
		"""Update the information within the grid"""

		self.ratingLabel.set_label("<big>" + str(float(movie.vote) * 10) + "%</big>")
		self.ratingBar.set_value(float(movie.vote))
		self.date.set_label("<big>" + movie.release_date + "</big>")
		self.runtime.set_label("<big>" +  str(int(movie.runtime) // 60) +
								" Hours " + str(int(movie.runtime) % 60) + " Minutes</big>")
		self.genres.set_label("<big>" + movie.get_genres_string() + "</big>")
		self.overview.set_label("<big>" + movie.overview + "</big>")


class InfoPage(Gtk.Box):
	"""Create a single page Notebook to display movie information"""

	def __init__(self, db, movieName):
		Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL, vexpand = True)

		self.db = db

		top = Gtk.Box(margin = 40, spacing = 50)

		self.movie = db.find_movie(movieName)

		self.action = ActBar(self.movie)
		self.poster = Gtk.Image(file = self.movie.get_large_image())
		self.grid = DetailsGrid(self.movie)

		top.add(self.poster)
		top.add(self.grid)

		self.pack_start(self.action, False, False, 0)
		self.pack_start(top, False, False, 0)

	def update(self, movieName):
		self.movie = self.db.find_movie(movieName)

		self.action.update(self.movie)
		self.poster.set_from_file(self.movie.get_large_image())
		self.grid.update(self.movie)
