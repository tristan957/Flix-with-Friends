import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GObject

import random

from Database import Database
from HeaderBar import HeaderBar
from SearchBar import SearchBar
from Info import InfoPage
from search_results import SearchResults


class LogIn(Gtk.Box):
    """Widget to grab initial log in information for the database"""

    __gsignals__ = {
        'credentials-set': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,))
    }

    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, margin=40,
                         spacing=30, halign=Gtk.Align.CENTER, valign=Gtk.Align.CENTER)

        self.cred_dict = {}

        header = Gtk.Label(label='<big><b>Enter the following information to begin</b></big>',
                           use_markup=True)
        self.check = Gtk.CheckButton(label='Click to enter a username and password if needed')
        self.check.connect('toggled', self.check_cb)

        locBox = Gtk.Box()
        locBox.get_style_context().add_class('linked')
        self.locBut = Gtk.Button(label='Enter')
        self.locBut.connect('clicked', self.grabLoc_cb)
        self.location = Gtk.Entry()
        self.location.connect('activate', self.grabLoc_cb)
        locBox.pack_start(self.location, True, True, 0)
        locBox.pack_end(self.locBut, False, True, 0)

        self.rev = Gtk.Revealer(transition_duration=300, transition_type=Gtk.RevealerTransitionType.CROSSFADE)
        revBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=30)

        userBox = Gtk.Box()
        userBox.get_style_context().add_class('linked')
        self.userBut = Gtk.Button(label='Enter')
        self.userBut.connect('clicked', self.grabUser_cb)
        self.userName = Gtk.Entry()
        self.userName.connect('activate', self.grabUser_cb)
        userBox.pack_start(self.userName, True, True, 0)
        userBox.pack_end(self.userBut, False, True, 0)

        passBox = Gtk.Box()
        passBox.get_style_context().add_class('linked')
        self.passBut = Gtk.Button(label='Enter')
        self.passBut.connect('clicked', self.grabPass_cb)
        self.password = Gtk.Entry(invisible_char_set=True)
        self.password.connect('activate', self.grabPass_cb)
        passBox.pack_start(self.password, True, True, 0)
        passBox.pack_end(self.passBut, False, True, 0)

        revBox.add(Gtk.Label(label='Enter a username', halign=Gtk.Align.START))
        revBox.add(userBox)
        revBox.add(Gtk.Label(label='Enter a password', halign=Gtk.Align.START))
        revBox.add(passBox)

        self.rev.add(revBox)

        self.pack_start(header, False, True, 0)
        self.pack_start(self.check, False, True, 0)
        self.pack_start(Gtk.Label(label='Enter a location for the database',
                                  halign=Gtk.Align.START), False, True, 0)
        self.pack_start(locBox, False, True, 0)
        self.pack_start(self.rev, False, True, 0)

    def check_cb(self, button):
        self.rev.set_reveal_child(button.get_active())

    def checkLength(self):
        """Check if all the credentials have been set"""

        if len(self.cred_dict) == 3 or (self.check.get_active() is False and len(self.cred_dict) == 1):
            self.emit('credentials-set', self.cred_dict)

    def grabLoc_cb(self, widget):
        """Grab the location of the server"""

        self.locBut.set_sensitive(False)
        self.location.set_sensitive(False)

        self.cred_dict['location'] = self.location.get_text()
        self.checkLength()

    def grabUser_cb(self, widget):
        """Grab the location of the server"""

        self.userBut.set_sensitive(False)
        self.userName.set_sensitive(False)

        self.cred_dict['username'] = self.userName.get_text()
        self.checkLength()

    def grabPass_cb(self, widget):
        """Grab the location of the server"""

        self.passBut.set_sensitive(False)
        self.password.set_sensitive(False)

        self.cred_dict['password'] = self.password.get_text()
        self.checkLength()


class InitWindow(Gtk.ApplicationWindow):
    """Gets the initial location information"""

    __gsignals__ = {
        "credentials-set": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,))
    }

    def __init__(self):
        Gtk.Window.__init__(self)

        header = Gtk.HeaderBar(title="Flix with Friends", show_close_button=True)
        self.set_titlebar(header)

        cred = LogIn()
        cred.connect("credentials-set", self.cred_cb)

        self.add(cred)

    def cred_cb(self, stack, cred_dict):
        self.emit("credentials-set", cred_dict)


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

        self.imdbBox = InfoPage(db, "Shrek")

        # stackBox.pack_end(self.imdbBox, True, True, 0)
        self.windowStack.add_named(self.imdbBox, "movie-info")

        credentials = LogIn()
        # locationChooser.connect("location-chosen", self.updateWin)
        self.windowStack.add_named(credentials, "credentials")

        box.add(self.searchBar)
        box.add(self.windowStack)

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
        movie_position = random.randint(0, len(movieResults) - 1)
        self.imdbBox.update(movieResults[movie_position].title)
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
        self.imdbBox.update(movieName)
        self.windowStack.set_visible_child_name("movie-info")
