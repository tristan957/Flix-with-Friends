import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject

import random
import re
import datetime


class GenrePop(Gtk.Popover):
    """Creates a popover to filter by genre"""

    __gsignals__ = {
        "genres-updated": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,))
    }

    def __init__(self, db):
        Gtk.Popover.__init__(self)

        self.genres = []

        box = Gtk.ButtonBox(orientation=Gtk.Orientation.VERTICAL)
        for genre in db.listGenres:
            button = Gtk.ModelButton(text=genre, role=Gtk.ButtonRole.CHECK,
                                     centered=False)
            box.add(button)
            button.connect("clicked", self.genre_cb)
        self.add(box)

    def genre_cb(self, button):
        button.set_property("active", not button.get_property("active"))
        if button.get_property("active") is True:
            self.genres.append(button.get_property("text"))
        else:
            self.genres.remove(button.get_property("text"))
        self.emit("genres-updated", self.genres)


class RatingPop(Gtk.Popover):
    """Creates a popover to filter by minimum rating"""

    __gsignals__ = {
        "rating-updated": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,))
    }

    def __init__(self):
        Gtk.Popover.__init__(self)

        self.scale = Gtk.Scale(draw_value=True, has_origin=True,
                               value_pos=0).new_with_range(Gtk.Orientation.HORIZONTAL, 0, 10, 1)
        self.scale.connect("value-changed", self.scale_cb)

        i = 1
        while i <= 10:
            self.scale.add_mark(i, Gtk.PositionType.TOP)
            i += 1
        self.scale.set_size_request(150, 40)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5, margin=5)
        label = Gtk.Label(label="Choose a\nminimum rating:", justify=Gtk.Justification.CENTER)

        box.add(label)
        box.add(self.scale)

        self.add(box)

    def scale_cb(self, scale):
        self.emit("rating-updated", scale.get_value())


class DatePop(Gtk.Popover):
    """Creates a popover to filter by release date"""

    __gsignals__ = {
        "switch-updated": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,)),
        "year-updated": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,))
    }

    def __init__(self, db):
        Gtk.Popover.__init__(self)

        self.switch = Gtk.Switch(active=False, state=False)
        self.switch.connect("state-set", self.switch_cb)

        self.combo = Gtk.ComboBoxText(wrap_width=4)
        self.combo.connect("changed", self.combo_cb)

        x = datetime.datetime.now().year
        while x >= db.oldest_year:
            self.combo.append_text(str(x))
            x -= 1
        self.combo.set_active(datetime.datetime.now().year - db.oldest_year)

        label = Gtk.Label(label="Search for movies produced\nonly in the year above",
                          justify=Gtk.Justification.CENTER)
        switchBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        switchBox.add(label)
        switchBox.add(self.switch)

        dateBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, margin=5, spacing=5)
        dateBox.add(self.combo)
        dateBox.add(switchBox)

        self.add(dateBox)

    def switch_cb(self, switch, state):
        self.emit("switch-updated", state)

    def combo_cb(self, combo):
        self.emit("year-updated", combo.get_active_text())


class ViewedByPop(Gtk.Popover):
    """Creates a popover to filter by who has seen the movie"""

    __gsignals__ = {
        "friends-updated": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,))
    }

    def __init__(self, db):
        Gtk.Popover.__init__(self)

        self.friends = []

        box = Gtk.ButtonBox(orientation=Gtk.Orientation.VERTICAL)
        for genre in db.viewers:
            button = Gtk.ModelButton(text=genre, role=Gtk.ButtonRole.CHECK,
                                     centered=False)
            box.add(button)
            button.connect("clicked", self.friend_cb)
        self.add(box)

    def friend_cb(self, button):
        button.set_property("active", not button.get_property("active"))
        if button.get_property("active") is True:
            self.friends.append(button.get_property("text"))
        else:
            self.friends.remove(button.get_property("text"))
        self.emit("friends-updated", self.friends)


class SearchBar(Gtk.Revealer):
    """Creates a search bar with an entry and filters"""

    __gsignals__ = {
        "search-ran": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,))
    }

    def __init__(self, db):
        Gtk.Revealer.__init__(self, transition_duration=300)

        self.entry = None

        self.db = db
        self.genres = []
        self.rating = 0
        self.switchState = False
        self.searchYear = db.oldest_year
        self.friends = []

        filters = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, margin=5) # box for the 4 search filters
        filters.get_style_context().add_class("linked")
        criteria = Gtk.Box()
        criteria.pack_start(filters, True, False, 0)
        criteria.get_style_context().add_class("inline-toolbar")

        self.set_property("child", criteria)

        self.entry = Gtk.SearchEntry()
        self.entry.set_can_focus(True)
        self.entry.set_size_request(250, -1)
        self.entry.connect("activate", self.entryUpdate_cb)
        self.entry.connect("changed", self.entryUpdate_cb)
        filters.pack_start(self.entry, True, True, 0)

        genrePop = GenrePop(db)
        ratingPop = RatingPop()
        datePop = DatePop(db)
        viewedByPop = ViewedByPop(db)

        genrePop.connect("genres-updated", self.genresUpdate_cb)
        ratingPop.connect("rating-updated", self.ratingUpdate_cb)
        datePop.connect("switch-updated", self.switchUpdate_cb)
        datePop.connect("year-updated", self.yearUpdate_cb)
        viewedByPop.connect("friends-updated", self.friendsUpdate_cb)

        # creating the menu buttons
        self.genreButton = Gtk.MenuButton(label="Genre", use_popover=True,
                                          popover=genrePop)
        self.genreButton.set_size_request(100, -1)
        self.ratingButton = Gtk.MenuButton(label="Rating", use_popover=True,
                                           popover=ratingPop)
        self.ratingButton.set_size_request(100, -1)
        self.dateButton = Gtk.MenuButton(label="Release Date", use_popover=True,
                                         popover=datePop)
        self.dateButton.set_size_request(100, -1)
        self.viewedByButton = Gtk.MenuButton(label="Never Seen By", use_popover=True,
                                             popover=viewedByPop)
        self.viewedByButton.set_size_request(100, -1)

        # connect the buttons to their callbacks
        self.genreButton.connect("toggled", self.showPopover_cb, genrePop)
        self.dateButton.connect("toggled", self.showPopover_cb, datePop)
        self.ratingButton.connect("toggled", self.showPopover_cb, ratingPop)
        self.viewedByButton.connect("toggled", self.showPopover_cb, viewedByPop)

        filters.pack_start(self.genreButton, True, True, 0)
        filters.pack_start(self.ratingButton, True, True, 0)
        filters.pack_start(self.dateButton, True, True, 0)
        filters.pack_end(self.viewedByButton, True, True, 0)

    def entryUpdate_cb(self, entry):
        self.run_search()

    def genresUpdate_cb(self, pop, genres):
        self.genres = genres
        self.run_search()

    def ratingUpdate_cb(self, pop, rating):
        self.rating = rating
        self.run_search()

    def switchUpdate_cb(self, pop, state):
        self.switchState = state
        self.run_search()

    def yearUpdate_cb(self, pop, year):
        self.searchYear = year
        self.run_search()

    def friendsUpdate_cb(self, pop, friends):
        self.friends = friends
        self.run_search()

    def showPopover_cb(self, button, pop):
        pop.show_all()

    def run_search(self, show=True): # put main windowStack on a revealer. if random movie is clicked set reveal to false. update imdbBox on Window regardless
    # -----------------
    # | search |	  |
    # | stack  | imdb |
    # -----------------
        """runs the search to get a list of relevant movies"""
        searchWord = self.entry.get_text()  # retrieve the content of the widget
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
            # if self.dateCombo.get_active() != -1:
            if str(self.searchYear) <= movie.release_date[:4]:
                if self.switchState:
                    if str(self.searchYear) == movie.release_date[:4]:
                        searchDate = True
                    else:
                        searchDate = False
                else:
                    searchDate = True
            else:
                searchDate = False
            # else:
            # 	searchDate = True

            # Check Rating
            if float(movie.vote) >= self.rating:
                searchRating = True

            # Check friends
            # Check how many matches for self genre are in Movie Genre
            # for f in self.friends:
            # 	for c in movie.viewers:
            # 		if f == c:
            # 			friendSearchCheck += 1
            searchFriend = True
            if len(self.friends) > 0:
                for f in self.friends:
                    for c in movie.viewers:
                        if f == c:
                            searchFriend = False

            # Make sure Number of genres in Movie match number of self genres
            # if friendSearchCheck == len(self.friends):
            # 	searchFriend = True

            # If passes checks, then print Movie info
            if ((searchTitle or searchDescription) and searchGenre and searchDate and searchRating and searchFriend):
                results.append(movie)

        # if update_search_view:
        # 	self.searchResults.set_search_view(results)
        # 	self.parent.stack.set_visible_child_name("search-results")
        # else:
        # 	self.parent.stack.set_visible_child_name("search-results")
        # 	return results
        if show is True:
            self.emit("search-ran", results)
        else:
            return results
