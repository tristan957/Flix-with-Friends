import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib, GdkPixbuf

import os
from Database import Database


class InfoWindow(Gtk.Window):

	"""
	Provide a popout window for a movie
	"""

	def __init__(self, movie):
		Gtk.Window.__init__(self)

		header = Gtk.HeaderBar(show_close_button = True, title = movie.title)
		self.set_titlebar(header)

		self.pop = Gtk.Popover(position = Gtk.PositionType.BOTTOM)
		popBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, margin = 5, spacing = 10)
		if len(movie.viewers) > 0:
			for friend in movie.viewers:
				popBox.add(Gtk.Label(label = friend))
		else:
			popBox.add(Gtk.Label(label = "No one has seen this movie."))
		self.pop.add(popBox)
		viewers = Gtk.MenuButton(label = "Viewers", use_popover = True, popover = self.pop)
		viewers.connect("toggled", self.viewers_cb)

		header.pack_end(viewers)

		self.add(DetailsGrid(movie))

		self.show_all()

	def viewers_cb(self, button):

		"""
		Toggles the popover
		"""

		self.pop.show_all()

class ActBar(Gtk.ActionBar):

	"""
	Provides a titlebar with actions for movies
	"""

	def __init__(self, movie):
		Gtk.ActionBar.__init__(self)

		self.movie = movie

		self.get_style_context().add_class("inline-toolbar")

		self.title = Gtk.Label(label = "<big><b>" + self.movie.title.replace('&', '&amp;') + "</b></big>", justify = Gtk.Justification.CENTER,
								use_markup = True)
		self.set_center_widget(self.title)

		# add a button to create a dialog that contains the movie info
		pageIcon = Gio.ThemedIcon(name = "view-paged-symbolic")
		popImage = Gtk.Image.new_from_gicon(pageIcon, Gtk.IconSize.BUTTON)
		popout = Gtk.Button(image = popImage)
		popout.connect("clicked", self.popout_cb)

		# add a button that has actions for the movie, like view trailer, view tmdb url for movie, and maybe an edit button??
		menuIcon = Gio.ThemedIcon(name = "open-menu-symbolic")
		menuImage = Gtk.Image.new_from_gicon(menuIcon, Gtk.IconSize.BUTTON)
		menu = Gtk.MenuButton(image = menuImage)

		# add a button to show a popover for who has seen the movie
		self.pop = Gtk.Popover(position = Gtk.PositionType.BOTTOM)
		self.popBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, margin = 5, spacing = 10)
		if len(self.movie.viewers) > 0:
			for friend in self.movie.viewers:
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

	def popout_cb(self, button):
		popout = InfoWindow(self.movie)

	def viewers_cb(self, button):

		"""
		Toggles the popover
		"""

		self.pop.show_all()

	def update(self, movie):

		"""
		Updates the data in the action bar
		"""

		self.movie = movie

		self.title.set_label("<big><b>" + self.movie.title.replace('&', '&amp;') + "</b></big>")

		# remake the popover box with new labels
		self.popBox.destroy()
		self.popBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, margin = 5, spacing = 10)
		if len(self.movie.viewers) > 0: # movies with no viewers for some reason have 1 viewer like "Aloha"
			for friend in self.movie.viewers:
				self.popBox.add(Gtk.Label(label = friend))
		else:
			self.popBox.add(Gtk.Label(label = "No one has seen this movie."))
		self.pop.add(self.popBox)

class GenreGrid(Gtk.Box):

	"""
	Container to display genres in an awesome layout_style
	"""

	def __init__(self, movie):
		Gtk.Box.__init__(self)

		self.grid = Gtk.Grid(row_spacing = 10, column_spacing = 10)

		row = 0
		column = 0
		for g in movie.genres:
			box = Gtk.Box()
			box.pack_start(Gtk.Label(label = "<big>" + g + "</big>",
								use_markup = True, halign = Gtk.Align.CENTER),
								True, True, 0)
			box.get_style_context().add_class('inline-toolbar')
			self.grid.attach(box, column, row, 1, 1)

			column+=1
			if column % 3 == 0:
				column = 0
				row+=1

		self.add(self.grid)
		self.show_all()

	def update(self, movie):
		self.grid.destroy()

		self.grid = Gtk.Grid(row_spacing = 10, column_spacing = 10)

		row = 0
		column = 0
		for g in movie.genres:
			box = Gtk.Box()
			box.pack_start(Gtk.Label(label = "<big>" + g + "</big>",
								use_markup = True, halign = Gtk.Align.CENTER),
								True, True, 0)
			box.get_style_context().add_class('inline-toolbar')
			self.grid.attach(box, column, row, 1, 1)

			column+=1
			if column % 3 == 0:
				column = 0
				row+=1

		self.add(self.grid)
		self.show_all()


class DetailsGrid(Gtk.Box):

	"""
	Create a container to display information in an organized fashion
	"""

	def __init__(self, movie):
		Gtk.Box.__init__(self, margin = 40, spacing = 50, halign = Gtk.Align.CENTER, valign = Gtk.Align.CENTER)

		self.poster = Gtk.Image(file = movie.get_large_image())
		self.poster.set_valign(Gtk.Align.START)

		grid = Gtk.Grid(column_spacing = 20, row_spacing = 10)

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
		self.genres = GenreGrid(movie)

		overviewTitle = Gtk.Label(label = "<big><b>Overview</b></big>", use_markup = True,
									halign = Gtk.Align.START)
		self.overview = Gtk.Label(label = "<big>" + movie.overview + "</big>", use_markup = True,
									halign = Gtk.Align.START, wrap = True, margin = 10)
		overviewScroll = Gtk.ScrolledWindow(shadow_type = Gtk.ShadowType.ETCHED_OUT, min_content_height = 250,
											window_placement = Gtk.CornerType.TOP_LEFT)
		overviewScroll.add(self.overview)

		self.peeps = PeopleView(movie)

		grid.attach(self.ratingLabel, 0, 0, 1, 1)
		grid.attach(self.ratingBar, 0, 1, 1, 3)
		grid.attach(dateTitle, 1, 0, 1, 1)
		grid.attach(self.date, 2, 0, 1, 1)
		grid.attach(runtimeTitle, 1, 1, 1, 1)
		grid.attach(self.runtime, 2, 1, 1, 1)
		grid.attach(genreTitle, 1, 2, 1, 1)
		grid.attach(self.genres, 2, 2, 1, 1)
		grid.attach(overviewTitle, 1, 3, 1, 1)
		grid.attach(overviewScroll, 2, 3, 1, 1)
		grid.attach(self.peeps, 0, 4, 3, 3)

		# box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
		# box.add(grid)
		# box.add(self.peeps)

		self.peeps.set_size_request(-1, 600)

		self.pack_start(self.poster, True, True, 0)
		self.pack_start(grid, True, True, 0)

	def update(self, movie):

		"""
		Update the information within the grid
		"""

		self.poster.set_from_file(movie.get_large_image())
		self.ratingLabel.set_label("<big>" + str(float(movie.vote) * 10) + "%</big>")
		self.ratingBar.set_value(float(movie.vote))
		self.date.set_label("<big>" + movie.release_date + "</big>")
		self.runtime.set_label("<big>" +  str(int(movie.runtime) // 60) +
								" Hours " + str(int(movie.runtime) % 60) + " Minutes</big>")
		self.genres.update(movie)
		self.overview.set_label("<big>" + movie.overview + "</big>")
		self.peeps.set_view(movie)

class PeopleView(Gtk.Grid):

	"""
	Create a view to show people associated with a movie
	"""

	def __init__(self, movie):
		Gtk.Grid.__init__(self, row_spacing = 10, column_spacing = 10)

		peeps = [movie.director]
		for peep in movie.allActors:
			peeps.append(peep)

		row = 0
		column = 0
		for peep in peeps:
			box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 5)
			role = ''
			if peep.role = 'actor':
				role = peep.charName
			else:
				role = peep.role.title()
			box.add()

class InfoPage(Gtk.Box):

	"""
	Create a single page Notebook to display movie information
	"""

	def __init__(self, db, movieName):
		Gtk.Box.__init__(self)

		self.db = db

		left = Gtk.Box()
		left.get_style_context().add_class('inline-toolbar')
		center = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, vexpand = True,
							halign = Gtk.Align.CENTER)
		right = Gtk.Box()
		right.get_style_context().add_class('inline-toolbar')

		self.movie = db.find_movie(movieName)

		self.action = ActBar(self.movie)
		# self.poster = Gtk.Image(file = self.movie.get_large_image())
		self.grid = DetailsGrid(self.movie)

		# top.add(self.poster)
		# top.add(self.grid)

		center.pack_start(self.action, False, False, 0)
		center.pack_start(self.grid, True, True, 0)

		self.pack_start(left, True, True, 0)
		self.pack_start(center, True, True, 0)
		self.pack_end(right, True, True, 0)

	def update(self, movieName):

		"""
		Update info within the InfoPage
		"""

		self.movie = self.db.find_movie(movieName)

		self.action.update(self.movie)
		self.grid.update(self.movie)

		self.queue_draw()
