import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
# from friends import addFriend, deleteFriend


class FriendDialog(Gtk.Dialog):

	def __init__(self, parent, action):
		Gtk.Dialog.__init__(self, action + " a Friend", parent, Gtk.DialogFlags.MODAL, use_header_bar = True)

		self.area = self.get_content_area()	 # area is a Gtk.Box
		box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
		box.get_style_context().add_class("linked")

		self.entry = Gtk.Entry(text = "Enter the name of a friend to " + action.lower())
		self.entry.grab_focus()
		self.entry.connect("activate", self.enterButton_cb, action)
		box.pack_start(self.entry, True, False, 0)

		self.enterButton = Gtk.Button(label = "Enter")
		self.enterButton.connect("clicked", self.enterButton_cb, action)
		box.pack_end(self.enterButton, True, False, 0)

		self.area.pack_start(box, True, False, 0)

		self.show_all()
		# if the action is deleting, create an autocompletion tree

	def enterButton_cb(self, enterButton, action):
		# if action is "Add":
		# 	addFriend(self.entry.get_text())
		# elif action is "Delete":
		# 	deleteFriend(self.entry.get_text())
		self.destroy()
