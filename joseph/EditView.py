import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class EditView(Gtk.TreeView):
    """Create an editable TreeView for the user to quickly and easily edit minor info about a movie"""

    def __init__(self, db): # cell renderer text is editable
        Gtk.TreeView.__init__(self)

class EditBox(Gtk.Box):
    """Create a container for a page to edit Movies"""

    def __init__(self, db):
        Gtk.Box.__init__(self)
