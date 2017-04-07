import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib

from Database import Database


class ActBar(Gtk.ActionBar):
	"""Provides a titlebar with actions for movies"""

	def __init__(self, movie):
		Gtk.ActionBar.__init__(self)

		self.title = Gtk.Label(label = movie.get_markup_title(), justify = Gtk.Justification.CENTER,
							use_markup = True, max_width_chars = 25, wrap = True)
		self.set_center_widget(self.title)

		pageIcon = Gio.ThemedIcon(name = "view-paged-symbolic")
		popImage = Gtk.Image.new_from_gicon(pageIcon, Gtk.IconSize.BUTTON)
		popout = Gtk.Button(image = popImage)
		# popout.connect("clicked", self.popout_cb)

		menuIcon = Gio.ThemedIcon(name = "open-menu-symbolic")
		menuImage = Gtk.Image.new_from_gicon(menuIcon, Gtk.IconSize.BUTTON)
		menu = Gtk.MenuButton(image = menuImage)

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

		self.pack_start(popout)
		self.pack_end(menu)
		self.pack_end(viewers)

	def viewers_cb(self, button):
		self.pop.show_all()

	def update(self, movie):
		self.title.set_label(movie.get_markup_title())

		self.popBox.destroy()
		self.popBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, margin = 5, spacing = 10)
		if len(movie.viewers) > 0: # movies with no viewers for some reason have 1 viewer like "Aloha"
			for friend in movie.viewers:
				self.popBox.add(Gtk.Label(label = friend))
		else:
			self.popBox.add(Gtk.Label(label = "No one has seen this movie."))
		self.pop.add(self.popBox)


class InfoPage(Gtk.Box):
	"""Create a single page Notebook to display movie information"""

	def __init__(self, db, movieName):
		Gtk.Box.__init__(self)

		self.db = db

		self.movie = db.find_movie(movieName)

		self.action = ActBar(self.movie)
		self.pack_start(self.action, False, False, 0)

	def update(self, movieName):
		self.movie = self.db.find_movie(movieName)

		self.action.update(self.movie)

		# self.title.set_label(self.movie.get_markup_title())
