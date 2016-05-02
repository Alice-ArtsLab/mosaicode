#!/usr/bin/env python
 # -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class SearchBar(Gtk.SearchBar):

    def __init__(self, main_window):
        Gtk.SearchBar.__init__(self)
        self.main_window = main_window

        self.search_entry = Gtk.SearchEntry()
        self.connect_entry(self.search_entry)
        self.add(self.search_entry)
        self.search_entry.connect("search-changed", self.search_changed)

        self.set_search_mode(True)
        self.show_all()

    def search_changed(self, data):
        self.main_window.main_control.search(self.search_entry.get_text())
        return self.search_entry.get_text()
        
    def show_search_bar(self):
        self.set_search_mode(True)
