import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from Window import Window


win = Window()	 # create the GUI
win.connect("delete-event", Gtk.main_quit)	 # when delete-event signal is received, calls Gtk.main_quit
win.show_all()	 # display the window and all widgets
Gtk.main()	 # continuous function for running GTK applications
