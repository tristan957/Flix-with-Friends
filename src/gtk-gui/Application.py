import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from Database import Database
from InitWindow import InitWindow2
from MainWindow import MainWindow


FLIX_APP_ID = "com.return0software.Flix-with-Friends"


class FlixApplication(Gtk.Application):
    """Acts a program manager"""

    initWindow = None
    mainWindow = None
    db = None

    def __init__(self):
        Gtk.Application.__init__(self, application_id=FLIX_APP_ID)

        self.connect("activate", self.activate_cb)
        self.connect("shutdown", self.shutdown_cb)

    def windowCheck(self):
        """Checks if a window is already in use"""

        if self.initWindow is None and self.mainWindow is None:
            self.initWindow = InitWindow2() # create the initial window to get a location
            self.initWindow.connect('cancel', self.quit)
            self.initWindow.connect("credentials-set", self.createMainWin)
            self.add_window(self.initWindow)
            # self.appWindow.connect("delete-event", Gtk.main_quit) # when delete-event signal is received, calls Gtk.main_quit

    def activate_cb(self, app):
        """Starts the program"""

        self.windowCheck()
        self.initWindow.show_all() # display the window and all widgets

    def createMainWin(self, win, cred_dict):
        """Creates the main window"""
        print('Hello')

        # Database.location = location
        self.db = Database(cred_dict) # create the database of the given location
        self.mainWindow = MainWindow(self.db) # create the main window now that we have an initial location
        self.remove_window(self.initWindow)
        self.initWindow.destroy()
        self.add_window(self.mainWindow)
        self.mainWindow.show_all()

    def shutdown_cb(self, app):
        app.quit() # analogous to self.quit
