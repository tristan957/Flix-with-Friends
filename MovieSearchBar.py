import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango
import re
from Database import Database
from Movie import get_image
from friends import getFriends
from search_results import SearchResults
import datetime


class MovieSearchBar(Gtk.Box):

	global results

	def __init__(self, location):
		Gtk.Box.__init__(self, orientation = Gtk.Orientation.HORIZONTAL)

		self.genres = []
		self.friends = []
		self.rating = 0
		self.db = Database(location)

		Database.fileName = location # FIXME move this to the parent class

		central = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, margin = 5)
		central.get_style_context().add_class("linked")

		self.searchEntry = Gtk.SearchEntry()
		self.searchEntry.grab_focus()
		central.pack_start(self.searchEntry, True, True, 0)

		# Callback for when enter key is pressed
		self.searchEntry.connect("activate", self.search_cb)
		self.searchEntry.connect("changed", self.search_cb)

		self.genrePopover = Gtk.Popover()
		self.genreBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		for genre in self.db.listGenres:
			butt = Gtk.ModelButton(text = genre, role = Gtk.ButtonRole.CHECK, centered = False)
			self.genreBox.add(butt)
			butt.connect("clicked", self.genresList_cb)
		self.genrePopover.add(self.genreBox)

		self.datePopover = Gtk.Popover()
		self.dateBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

		# store = Gtk.ListStore(str)
		self.dateCombo = Gtk.ComboBoxText(wrap_width = 4)
		self.dateCombo.connect("changed", self.search_cb)

		x = datetime.datetime.now().year
		while x >= self.db.oldest_year:
			self.dateCombo.append_text(str(x))
			x -= 1
		self.dateCombo.set_active(-1)
		# print(self.dateCombo.get_active_text())

		# renderer = Gtk.CellRendererText()
		# self.dateCombo.pack_start(renderer, True)
		# self.dateCombo.add_attribute(renderer, "text", 0)

		self.dateAfter = Gtk.Switch()
		dateLabel = Gtk.Label(label = "Search for movies produced\nonly in the year above", justify = Gtk.Justification.CENTER)
		switchBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 10)
		switchBox.add(self.dateAfter)
		switchBox.add(dateLabel)
		# self.dateBox.add(self.dateEntry)
		self.dateBox.add(self.dateCombo)
		self.dateBox.add(switchBox)
		self.datePopover.add(self.dateBox)

		self.viewedByPopover = Gtk.Popover()
		viewedByBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		for friend in self.db.friends:
			butt = Gtk.ModelButton(text = friend, role = Gtk.ButtonRole.CHECK, centered = False)
			viewedByBox.add(butt)
			butt.connect("clicked", self.friendsList_cb)
		self.viewedByPopover.add(viewedByBox)

		self.ratingPopover = Gtk.Popover()
		ratingBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 5, margin = 5)
		ratingLabel = Gtk.Label(label = "Choose a\nminimum rating:", justify = Gtk.Justification.CENTER)
		self.scale = Gtk.Scale(draw_value = True, has_origin = True).new_with_range(Gtk.Orientation.HORIZONTAL, 0, 10, 1)
		self.scale.connect("value-changed", self.minRating_cb)
		i = 1
		while i <= 10:
			self.scale.add_mark(i, Gtk.PositionType.TOP)
			i = i + 1
		self.scale.set_size_request(150, 40)
		ratingBox.add(ratingLabel)
		ratingBox.add(self.scale)
		self.ratingPopover.add(ratingBox)

		self.genreButton = Gtk.MenuButton(label = "Genre", use_popover = True, popover = self.genrePopover)
		self.dateButton = Gtk.MenuButton(label = "Release Date", use_popover = True, popover = self.datePopover)
		self.viewedByButton = Gtk.MenuButton(label = "Viewed By", use_popover = True, popover = self.viewedByPopover)
		self.ratingButton = Gtk.MenuButton(label = "Rating", use_popover = True, popover = self.ratingPopover)

		central.pack_start(self.genreButton, True, True, 0)
		central.pack_start(self.dateButton, True, True, 0)
		central.pack_start(self.viewedByButton, True, True, 0)
		central.pack_end(self.ratingButton, True, True, 0)

		self.genreButton.connect("toggled", self.genre_cb)
		self.dateButton.connect("toggled", self.releaseDate_cb)
		self.viewedByButton.connect("toggled", self.viewedBy_cb)
		self.ratingButton.connect("toggled", self.rating_cb)

		self.pack_start(central, True, False, 0)
		self.get_style_context().add_class("inline-toolbar")

		# self.searchResults = SearchResults()

	def search_cb(self, widget):
		self.run_search()

	def genresList_cb(self, genreButton):
		genreButton.props.active = not genreButton.props.active
		if genreButton.props.active is True:
			self.genres.append(genreButton.props.text)
		else:
			self.genres.remove(genreButton.props.text)
		self.run_search()

	def friendsList_cb(self, friendButton):
		friendButton.props.active = not friendButton.props.active
		if friendButton.props.active is True:
			self.friends.append(friendButton.props.text)
			print(self.friends)
		else:
			self.friends.remove(friendButton.props.text)
		self.run_search()

	def minRating_cb(self, scale):
		self.rating = scale.get_value()
		self.run_search()

	def genre_cb(self, genreButton):
		self.genrePopover.show_all()

	def releaseDate_cb(self, dateButton):
		self.datePopover.show_all()

	def viewedBy_cb(self, viewedByButton):
		self.viewedByPopover.show_all()

	def rating_cb(self, ratingButton):
		self.ratingPopover.show_all()

	def run_search(self):
		searchWord = self.searchEntry.get_text()  # retrieve the content of the widget

		for movie in self.db.movies:
			# Check if search word passes regex check for either Movie title or description
			searchTitle = bool((re.search(searchWord, movie.title, re.M | re.I))) or (searchWord == '')
			searchDescription = bool((re.search(searchWord, movie.overview, re.M | re.I)))

			genreSearchCheck = 0
			searchGenre = 0
			searchRating = 0

			# Check how many matches for self genre are in Movie Genre
			for g in self.genres:
				for c in movie.genres:
					if g == c:
						genreSearchCheck += 1

			# Make sure Number of genres in Movie match number of self genres
			if genreSearchCheck == len(self.genres):
				searchGenre = True

			# print(self.dateCombo.get_active_text())
			if self.dateCombo.get_active() != -1:
				if self.dateCombo.get_active_text() <= movie.release_date[:4]:
					if self.dateAfter.get_active():
						if self.dateCombo.get_active_text() == movie.release_date[:4]:
							searchDate = True
						else:
							searchDate = False
					else:
						searchDate = True
				else:
					searchDate = False
			else:
				searchDate = True

			# Check Rating
			if float(movie.vote) >= self.scale.get_value():
				searchRating = True

			# If passes checks, then print Movie info
			if ((searchTitle or searchDescription) and searchGenre and searchDate and searchRating):
				print("Title:", movie.title)
				print("Release Date:", movie.release_date)
				print("Rating:", movie.vote)
				print("Runtime:", movie.runtime)
				print("Genres:", end=" ")
				for i in range(0, len(movie.genres)):
					print(movie.genres[i], end = " ")
				print("")
				print("Overview:", movie.overview)
				print("Viewers:", end=" ")
				for i in range(0, len(movie.viewers)):
					print(movie.viewers[i], end=" ")
				# GOing to need a try except for this,
				# get_image(movie.poster_path, movie.title)
				print('\n')

		# self.searchResults.set_search_view()
