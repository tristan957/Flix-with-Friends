import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GObject

import random

from Database import Database
from HeaderBar import HeaderBar
from SearchBar import SearchBar
from Info2 import InfoPage
from search_results import SearchResults


class MainWindow(Gtk.ApplicationWindow):

    """
    Window where all the magic happens
    """

    # start with the revealers hidden, then cover up getting started screen with revealers (maybe even hide the background label)
    # ____________________________________
    # | results | getting | info         |
    # | on	  | started | page 		   |
    # | revealer| screen  | on revealer  |
    # |_________|_________|______________|

    def __init__(self, db):
        Gtk.Window.__init__(self)

        self.db = db
        self.windowStack = None
        self.revealer = None
        self.headerBar = None
        self.searchBar = None
        self.imdbBox = None
        self.searchResults = None

        self.connect("key-press-event", self.key_pressed_cb)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # stackBox = Gtk.Box()

        self.windowStack = Gtk.Stack(interpolate_size=True,
                                     transition_type=Gtk.StackTransitionType.CROSSFADE)

        self.header = HeaderBar(self, self.db)
        self.header.connect('go-back', self.goBack_cb)
        self.header.connect("random-clicked", self.random_cb)
        self.header.connect("revealer-change", self.reveal_cb)
        self.header.connect('source-change', self.sourceChange_cb)
        self.set_titlebar(self.header)

        self.searchBar = SearchBar(db)
        self.searchBar.connect("search-ran", self.searchRan_cb)

        self.searchResults = SearchResults()
        self.searchResults.connect("row-activated", self.updateIMDB_cb)
        # self.windowStack.add_named(self.searchResults, "search-results")

        # stackBox.pack_start(self.searchResults, False, False, 0)
        self.windowStack.add_named(self.searchResults, "search-results") # what if I implement the infobox on a stack that also includes a start typing page like the search results has right now and a choose a search result to display detailed info page

        self.windowStack.set_visible_child_name("search-results")

        self.imdbBox = InfoPage(db.find_movie("Shrek"))
        self.imdbBox.set_size_request(700, 700)

        # stackBox.pack_end(self.imdbBox, True, True, 0)
        self.windowStack.add_named(self.imdbBox, "movie-info")

        # credentials = LogIn()
        # locationChooser.connect("location-chosen", self.updateWin)
        # self.windowStack.add_named(credentials, "credentials")

        box.pack_start(self.searchBar, False, True, 0)
        box.pack_end(self.windowStack, True, True, 0)

        self.add(box)

    def goBack_cb(self, headerBar):
        self.windowStack.set_visible_child_name('search-results')

    def key_pressed_cb(self, win, event):
        self.searchBar.set_transition_type(Gtk.RevealerTransitionType.SLIDE_DOWN)
        self.searchBar.set_reveal_child(True)
        self.header.search.set_active(True)
        if self.searchBar.entry.has_focus() is False:
            self.searchBar.entry.grab_focus()
        return self.searchBar.entry.handle_event(event)

    def updateSource(self, locationChooser, location):
        # Database.location = location
        self.show_all()

    def random_cb(self, header):
        self.windowStack.set_visible_child_name("movie-info")
        movieResults = self.searchBar.run_search(False)
        movie_position = random.randint(0, len(movieResults) - 1) # make this a db_function to return a random movie
        self.imdbBox.update(self.db.find_movie(movieResults[movie_position].title))
        # self.searchBar.run_search()

    def reveal_cb(self, header, toggled):
        if toggled is True:
            self.searchBar.set_transition_type(Gtk.RevealerTransitionType.SLIDE_DOWN)
            self.searchBar.set_reveal_child(True)
            if self.searchBar.entry.has_focus() is False:
                self.searchBar.entry.grab_focus()
        else:
            self.searchBar.set_transition_type(Gtk.RevealerTransitionType.SLIDE_UP)
            self.searchBar.set_reveal_child(False)
            # self.grab_focus()

    def searchRan_cb(self, searchBar, results):
        self.searchResults.set_search_view(results)
        self.windowStack.set_visible_child_name("search-results")

    def sourceChange_cb(self, header):
        self.windowStack.set_visible_child_name('credentials')

    def updateIMDB_cb(self, searchResults, movieName):
        self.imdbBox.update(self.db.find_movie(movieName))
        self.windowStack.set_visible_child_name("movie-info")
