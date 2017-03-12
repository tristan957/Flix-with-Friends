import gi
gi.require_version('Gtk', '3.0')
import random
import re
import datetime
from gi.repository import Gtk, Pango
from Database import Database
from friends import getFriends
from search_results import SearchResults
from MovieBox import MovieBox


class MovieSearchBar(Gtk.Revealer):

	def __init__(self, location, parent):
		Gtk.Box.__init__(self, transition_duration = 300)

		self.parent = parent
		self.genres = []
		self.friends = []
		self.db = Database(location)
		Database.fileName = location # FIXME move this to the parent class

		random.seed()

		self.imdbBox = MovieBox(None)
		self.searchResults = SearchResults(self)
		searchPage = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 4)
		searchPage.pack_start(self.searchResults, False, False, 0)
		searchPage.pack_end(self.imdbBox, False, False, 0)

		searchCriteria = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
		self.parent.stack.add_named(searchPage, "search-results")

		filters = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, margin = 5)
		filters.get_style_context().add_class("linked")

		self.searchEntry = Gtk.SearchEntry()
		self.searchEntry.set_can_focus(True)
		self.searchEntry.set_size_request(250, -1)
		filters.pack_start(self.searchEntry, True, True, 0)
		# Callback for when enter key is pressed
		self.searchEntry.connect("activate", self.search_cb)
		self.searchEntry.connect("changed", self.search_cb)

		self.genrePopover = Gtk.Popover()
		genreBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		for genre in self.db.listGenres:
			butt = Gtk.ModelButton(text = genre, role = Gtk.ButtonRole.CHECK, centered = False)
			genreBox.add(butt)
			butt.connect("clicked", self.genresList_cb)
		self.genrePopover.add(genreBox)

		self.ratingPopover = Gtk.Popover()
		ratingBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 5, margin = 5)
		ratingLabel = Gtk.Label(label = "Choose a\nminimum rating:", justify = Gtk.Justification.CENTER)
		self.scale = Gtk.Scale(draw_value = True, has_origin = True, value_pos = 0).new_with_range(Gtk.Orientation.HORIZONTAL, 0, 10, 1)
		self.scale.connect("value-changed", self.search_cb)
		i = 1
		while i <= 10:
			self.scale.add_mark(i, Gtk.PositionType.TOP)
			i = i + 1
		self.scale.set_size_request(150, 40)
		ratingBox.add(ratingLabel)
		ratingBox.add(self.scale)
		self.ratingPopover.add(ratingBox)

		self.datePopover = Gtk.Popover()
		dateBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		self.dateAfter = Gtk.Switch(active = False, state = False)
		self.dateAfter.connect("state-set", self.switch_cb)
		dateLabel = Gtk.Label(label = "Search for movies produced\nonly in the year above", justify = Gtk.Justification.CENTER)
		switchBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 10)
		switchBox.add(self.dateAfter)
		switchBox.add(dateLabel)
		self.dateCombo = Gtk.ComboBoxText(wrap_width = 4)
		self.dateCombo.connect("changed", self.search_cb)
		x = datetime.datetime.now().year
		while x >= self.db.oldest_year:
			self.dateCombo.append_text(str(x))
			x -= 1
		self.dateCombo.set_active(datetime.datetime.now().year - self.db.oldest_year);
		dateBox.add(self.dateCombo)
		dateBox.add(switchBox)
		self.datePopover.add(dateBox)

		self.viewedByPopover = Gtk.Popover()
		viewedByBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		for friend in self.db.friends:
			butt = Gtk.ModelButton(text = friend, role = Gtk.ButtonRole.CHECK, centered = False)
			viewedByBox.add(butt)
			butt.connect("clicked", self.friendsList_cb)
		self.viewedByPopover.add(viewedByBox)

		self.genreButton = Gtk.MenuButton(label = "Genre", use_popover = True, popover = self.genrePopover)
		self.genreButton.set_size_request(100, -1)
		self.ratingButton = Gtk.MenuButton(label = "Rating", use_popover = True, popover = self.ratingPopover)
		self.ratingButton.set_size_request(100, -1)
		self.dateButton = Gtk.MenuButton(label = "Release Date", use_popover = True, popover = self.datePopover)
		self.dateButton.set_size_request(100, -1)
		self.viewedByButton = Gtk.MenuButton(label = "Viewed By", use_popover = True, popover = self.viewedByPopover)
		self.viewedByButton.set_size_request(100, -1)

		filters.pack_start(self.genreButton, True, True, 0)
		filters.pack_start(self.ratingButton, True, True, 0)
		filters.pack_start(self.dateButton, True, True, 0)
		filters.pack_end(self.viewedByButton, True, True, 0)

		self.genreButton.connect("toggled", self.genre_cb)
		self.dateButton.connect("toggled", self.releaseDate_cb)
		self.ratingButton.connect("toggled", self.rating_cb)
		self.viewedByButton.connect("toggled", self.viewedBy_cb)

		searchCriteria.pack_start(filters, True, False, 0)
		searchCriteria.get_style_context().add_class("inline-toolbar")

		self.set_property("child", searchCriteria)

	def genresList_cb(self, genreButton):
		genreButton.set_property("active", not genreButton.get_property("active"))
		if genreButton.get_property("active") is True:
			self.genres.append(genreButton.get_property("text"))
		else:
			self.genres.remove(genreButton.get_property("text"))
		self.run_search()

	def friendsList_cb(self, friendButton):
		friendButton.set_property("active", not friendButton.get_property("active"))
		if friendButton.get_property("active") is True:
			self.friends.append(friendButton.get_property("text"))
		else:
			self.friends.remove(friendButton.get_property("text"))
		self.run_search()

	def randomMovieButton_cb(self, randomMovieButton,parent):
		movieResults = self.run_search(False)
		number_movies = len(movieResults) - 1
		movie_position = random.randint(0, number_movies)

		movie = movieResults[movie_position]
		parent.searchBar.imdbBox.update(movie.title)
		print("Title:", movie.title)
		print("Release Date:", movie.release_date)
		print("Rating:", movie.vote)
		print("Runtime:", movie.runtime)
		print("Genres:", end = " ")
		for i in range(0, len(movie.genres)):
			print(movie.genres[i], end = " ")
		print("")
		print("Overview:", movie.overview)
		# GOing to need a try except for this,
		# movie.get_image(movie.poster_path, movie.title)
		print('')

	def search_cb(self, widget):
		self.run_search()

	def switch_cb(self, switch, state):
		self.run_search()

	def genre_cb(self, genreButton):
		self.genrePopover.show_all()

	def releaseDate_cb(self, dateButton):
		self.datePopover.show_all()

	def viewedBy_cb(self, viewedByButton):
		self.viewedByPopover.show_all()

	def rating_cb(self, ratingButton):
		self.ratingPopover.show_all()

	def run_search(self, update_search_view=True):
		searchWord = self.searchEntry.get_text()  # retrieve the content of the widget
		results = []

		for movie in self.db.movies:
			# Check if search word passes regex check for either Movie title or description
			searchTitle = bool((re.search(searchWord, movie.title, re.M | re.I))) or (searchWord == '')
			searchDescription = bool((re.search(searchWord, movie.overview, re.M | re.I)))

			genreSearchCheck = 0
			searchGenre = 0
			searchRating = 0
			friendSearchCheck = 0
			searchFriend = 0


			# Check how many matches for self genre are in Movie Genre
			for g in self.genres:
				for c in movie.genres:
					if g == c:
						genreSearchCheck += 1

			# Make sure Number of genres in Movie match number of self genres
			if genreSearchCheck == len(self.genres):
				searchGenre = True

			# Check to see if date search criteria match
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

			# Check friends
			# Check how many matches for self genre are in Movie Genre
			for f in self.friends:
				for c in movie.viewers:
					if f == c:
						friendSearchCheck += 1

			# Make sure Number of genres in Movie match number of self genres
			if friendSearchCheck == len(self.friends):
				searchFriend = True


			# If passes checks, then print Movie info
			if ((searchTitle or searchDescription) and searchGenre and searchDate and searchRating and searchFriend):
				results.append(movie)

		# if update_search_view:
		self.searchResults.set_search_view(results)
		self.parent.stack.set_visible_child_name("search-results")
		# else:
		return results
