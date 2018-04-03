#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa: E402
"""
This module contains the TreeView class.
"""
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')
from gi.repository import Gtk

class TreeView(Gtk.ScrolledWindow):
    """
    This class contains methods related the TreeView class
    """

    # ----------------------------------------------------------------------
    def __init__(self, title, action, data=None):
        Gtk.ScrolledWindow.__init__(self)
        self.list_store = Gtk.ListStore(str)
        self.tree_view = Gtk.TreeView(self.list_store)
        self.tree_view.connect("row-activated", action, data)
        self.add(self.tree_view)
        col = Gtk.TreeViewColumn(title)
        self.tree_view.append_column(col)
        cellrenderertext = Gtk.CellRendererText()
        col.pack_end(cellrenderertext, True)
        col.add_attribute(cellrenderertext, "text", 0)

    # ----------------------------------------------------------------------
    def populate(self, item_list):
        self.list_store.clear()
        for item in item_list:
            self.list_store.append([item])

    # ----------------------------------------------------------------------
    def get_selection(self):
        return self.tree_view.get_selection()

