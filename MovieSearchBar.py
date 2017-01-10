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

		self.genres = []
		self.friends = getFriends()
		self.db = Database(location)

		self.search = Gtk.SearchBar(search_mode_enabled = True, show_close_button = True)
		self.searchEntry = Gtk.SearchEntry()
		self.search.connect_entry(self.searchEntry)
		self.searchEntry.grab_focus()
		self.add(self.searchEntry)

		# Callback for when enter key is pressed
		self.searchEntry.connect("activate", self.search_cb, self.db)
		self.searchEntry.connect("search-changed", self.search_cb, self.db)

		self.genrePopover = Gtk.Popover()
		self.genreBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		for genre in self.db.listGenres:
			butt = Gtk.CheckButton(label = genre)
			self.genreBox.add(butt)
			butt.connect("toggled", self.genresList_cb)
		self.genrePopover.add(self.genreBox)

		self.datePopover = Gtk.Popover()
		self.dateBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		self.dateEntry = Gtk.Entry()
		self.dateEntry.set_text("Enter a year")
		self.dateAfter = Gtk.Switch()
		self.dateLabel = Gtk.Label(label = "Search for movies produced\nonly in the year above", justify = Gtk.Justification.CENTER)
		self.switchBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 10)
		self.switchBox.add(self.dateAfter)
		self.switchBox.add(self.dateLabel)
		self.dateBox.add(self.dateEntry)
		self.dateBox.add(self.switchBox)
		self.datePopover.add(self.dateBox)

		self.viewedByPopover = Gtk.Popover()
		self.viewedByBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		for friend in self.friends:
			butt = Gtk.CheckButton(label = friend)
			self.viewedByBox.add(butt)
			butt.connect("toggled", self.friendsList_cb)
		self.viewedByPopover.add(self.viewedByBox)

		self.genreButton = Gtk.MenuButton(label = "Genre", use_popover = True, popover = self.genrePopover)
		self.dateButton = Gtk.MenuButton(label = "Release Date", use_popover = True, popover = self.datePopover)
		self.viewedByButton = Gtk.MenuButton(label = "Viewed By", use_popover = True, popover = self.viewedByPopover)
		self.ratingButton = Gtk.ToggleButton(label = "Rating")

		self.buttonBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 2)
		self.buttonBox.add(self.genreButton)
		self.buttonBox.add(self.dateButton)
		self.buttonBox.add(self.viewedByButton)
		self.buttonBox.add(self.ratingButton)

		self.genreButton.connect("toggled", self.genre_cb)
		self.dateButton.connect("toggled", self.releasedBy_cb)
		self.viewedByButton.connect("toggled", self.viewedBy_cb)
		# self.ratingButton.connect("toggled", self.searchCategories_cb)

		self.add(self.buttonBox)

	def genresList_cb(self, genreButton):
		if genreButton.get_active() is True:
			self.genres.append(genreButton.get_label())
		else:
			self.genres.remove(genreButton.get_label())

	def friendsList_cb(self, friendButton):
		if friendButton.get_active() is True:
			self.friends.remove(friendButton.get_label())
			print(self.friends)
		else:
			self.friends.append(friendButton.get_label())

	def search_cb(self, entry, db):
		# retrieve the content of the widget
		self.run_search(entry, db)

	def genre_cb(self, genreButton):
		self.genrePopover.show_all()

	def releasedBy_cb(self, dateButton):
		self.datePopover.show_all()

	def viewedBy_cb(self, viewedByButton):
		self.viewedByPopover.show_all()

	def run_search(self, entry, db):
		searchWord = entry.get_text()  # retrieve the content of the widget
		# create new DB object from global location


		for movie in db.movies:
			ratingSearchCheck = 0
			searchTitle = bool((re.search(searchWord, movie.title, re.M | re.I))) or (searchWord == '')
			searchDescription = bool((re.search(searchWord, movie.overview, re.M | re.I)))
			# searchRelease = bool((re.search(searchWord, movie.release_date, re.M | re.I))) and releaseSearch
			# searchRating = (str(movie.vote) >= str(searchWord)) and ratingSearch

			ratingSearchCheck = 0
			searchGenre = 0

			for g in self.genres:
				for c in movie.genres:
					if g == c:
						ratingSearchCheck += 1

			if ratingSearchCheck == len(self.genres):
				searchGenre = True


			if ((searchTitle or searchDescription) and searchGenre):
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
