#!/usr/bin/env python
 # -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class SearchBar(Gtk.Box, Gtk.SearchBar):

    def __init__(self, main_window):
        super(SearchBar, self).__init__()

        self.main_window = main_window
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.connect("search-changed", self.search_changed)
        self.pack_start(self.search_entry,True, True, 0)

    def search_changed(self, data):
        self.main_window.main_control.search(self.search_entry.get_text())
        return self.search_entry.get_text()
