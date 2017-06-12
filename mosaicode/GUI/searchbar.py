#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This modules contains the SearchBar class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class SearchBar(Gtk.Box, Gtk.SearchBar):
    """
    This class contains methods related the SearchBar class.
    """

    # ----------------------------------------------------------------------

    def __init__(self, main_window):
        super(SearchBar, self).__init__()

        self.main_window = main_window
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.connect("search-changed", self.search_changed)
        self.pack_start(self.search_entry, True, True, 0)

    # ----------------------------------------------------------------------
    def search_changed(self, data):
        """
        This method monitors if search was search_changed.
            Parameter:
            Returns:
                * **SearchBar** (:class:`SearchBar<mosaicode.GUI.searchbar>`)
        """
        self.main_window.main_control.search(
            self.search_entry.get_text().upper())
        return self.search_entry.get_text()
# ---------------------------------------------------------------------------
