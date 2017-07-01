import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
# from friends import addFriend, deleteFriend


class FriendDialog(Gtk.Dialog):

    """
    Dialog for adding and deleting friends
    """

    __gsignals__ = {
        "friend-added": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,)), # in conjunction with change source button to change the database source
        "friend-deleted": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,)) # in conjunction with edit source button to bring up an edit screen
    }

    def __init__(self, parent, action):
        Gtk.Dialog.__init__(self, action + " a Friend", parent, Gtk.DialogFlags.MODAL, use_header_bar=True)

        self.area = self.get_content_area()	 # area is a Gtk.Box
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box.get_style_context().add_class("linked")

        label = Gtk.Label(label="Enter the name of a friend to " + action.lower())
        self.area.pack_start(label, True, True, 0)

        self.entry = Gtk.Entry()
        self.entry.grab_focus()
        self.entry.connect("activate", self.enterButton_cb, action)
        box.pack_start(self.entry, True, False, 0)

        self.enterButton = Gtk.Button(label="Enter")
        self.enterButton.connect("clicked", self.enterButton_cb, action)
        box.pack_end(self.enterButton, True, False, 0)

        self.area.pack_start(box, True, False, 0)

        self.show_all()
        # if the action is deleting, create an autocompletion tree

    def enterButton_cb(self, enterButton, action):
        if action == "Add":
            self.emit("friend-added", self.entry.get_text())
        elif action == "Delete":
            self.emit("friend-deleted", self.entry.get_text())
        self.destroy()
