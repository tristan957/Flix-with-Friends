import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import re
from Database import Database
from Movie import get_image
from friends import getFriends


class MovieSearchBar(Gtk.Box):

	def __init__(self, location):
		Gtk.Box.__init__(self, orientation = Gtk.Orientation.HORIZONTAL, spacing = 50)

		self.categories = []
		self.db = Database(location)
		print(location)
		print(self.db.listGenres)

		self.search = Gtk.SearchBar(search_mode_enabled = True, show_close_button = True)
		self.entry = Gtk.SearchEntry()
		self.search.connect_entry(self.entry)
		self.entry.grab_focus()
		self.add(self.entry)

		# Callback for when enter key is pressed
		self.entry.connect("activate", self.search_cb, self.db)
		self.entry.connect("search-changed", self.search_changed_cb, self.db)

		self.categories.append("Name")

		self.genrePopover = Gtk.Popover()
		self.genreBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		for genre in self.db.listGenres:
			self.genreBox.add(Gtk.CheckButton(label = genre))
			print(genre)
		self.genrePopover.add(self.genreBox)

		self.viewedByPopover = Gtk.Popover()
		self.viewedByBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		friendsList = getFriends()
		for friend in friendsList:
			self.viewedByBox.add(Gtk.CheckButton(label = friend))
		self.viewedByPopover.add(self.viewedByBox)

		self.nameButton = Gtk.ToggleButton(label = "Name", active = True)
		self.descriptionButton = Gtk.ToggleButton(label = "Description")
		self.genreButton = Gtk.MenuButton(label = "Genre", use_popover = True, popover = self.genrePopover)
		self.dateButton = Gtk.ToggleButton(label = "Release Date")
		self.viewedByButton = Gtk.MenuButton(label = "Viewed By", use_popover = True, popover = self.viewedByPopover)
		self.ratingButton = Gtk.ToggleButton(label = "Rating")

		self.buttonBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 2)
		self.buttonBox.add(self.nameButton)
		self.buttonBox.add(self.descriptionButton)
		self.buttonBox.add(self.genreButton)
		self.buttonBox.add(self.dateButton)
		self.buttonBox.add(self.viewedByButton)
		self.buttonBox.add(self.ratingButton)

		self.nameButton.connect("toggled", self.searchCategories_cb)
		self.descriptionButton.connect("toggled", self.searchCategories_cb)
		self.genreButton.connect("toggled", self.searchCategories_cb)
		self.dateButton.connect("toggled", self.searchCategories_cb)
		self.viewedByButton.connect("clicked", self.viewedBy_cb)
		self.ratingButton.connect("toggled", self.searchCategories_cb)

		self.add(self.buttonBox)

	def searchCategories_cb(self, searchButton):
		if searchButton.get_active() is True:
			self.categories.append(searchButton.get_label())
			print(self.categories)
		else:
			self.categories.remove(searchButton.get_label())
			print(self.categories)

	def getCategories(self):
		return self.categories

	def search_cb(self, entry, db):
		# retrieve the content of the widget
		print(entry.get_text())
		self.run_search(entry, db)

	def search_changed_cb(self, entry, db):
		print(entry.get_text())
		self.run_search(entry, db)

	def viewedBy_cb(self, viewedByButton):
		self.viewedByPopover.show_all()

	def run_search(self, entry, db):
		searchWord = entry.get_text()  # retrieve the content of the widget
		# create new DB object from global location

		titleSearch = 0
		descriptionSearch = 0
		genreSearch = 0
		releaseSearch = 0
		ratingSearch = 0
		genreSearch = 0

		# If Value selected for search
		if any("Name" in s for s in self.categories):
			titleSearch = 1

		if any("Description" in s for s in self.categories):
			descriptionSearch = 1

		if any("Release Date" in s for s in self.categories):
			releaseSearch = 1

		if any("Rating" in s for s in self.categories):
			ratingSearch = 1

		if any("Genre" in s for s in self.categories):
			genreSearch = 1

		print(db.listGenres)
		for movie in db.movies:
			ratingSearchCheck = 0
			searchTitle = bool((re.search(searchWord, movie.title, re.M | re.I))) and titleSearch
			searchDescription = bool((re.search(searchWord, movie.overview, re.M | re.I))) and descriptionSearch
			searchRelease = bool((re.search(searchWord, movie.release_date, re.M | re.I))) and releaseSearch
			searchRating = (str(movie.vote) >= str(searchWord)) and ratingSearch

			if any(searchWord.upper() in s.upper() for s in movie.genres):
				ratingSearchCheck = 1
			searchGenre = ratingSearchCheck and genreSearch

			if searchTitle or searchDescription or searchRelease or searchRating or searchGenre:
				print("Title:", movie.title)
				print("Release Date:", movie.release_date)
				print("Rating:", movie.vote)
				print("Runtime:", movie.runtime)
				print("Genres:", end=" ")
				for i in range(0, len(movie.genres)):
					print(movie.genres[i], end=" ")
				print("")
				print("Overview:", movie.overview)
				get_image(movie.poster_path, movie.title)
