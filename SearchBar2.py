import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import random
import re
import datetime


class SearchBar(Gtk.Revealer):
	"""Creates a search bar with an entry and filters"""
	def __init__(self):
		Gtk.Revealer.__init__(self, transition_duration = 300)

		self.entry = None

		self.genres = []
		self.friends = []

		criteria = Gtk.Box(margin = 5)
		filters = Gtk.ButtonBox(layout_style = Gtk.ButtonBoxStyle.EXPAND)

		self.entry = Gtk.SearchEntry()
		self.entry.set_can_focus(True)
		self.entry.set_size_request(250, -1)
		self.entry.connect("activate", self.search_cb)
		self.entry.connect("change", self.search_cb)
