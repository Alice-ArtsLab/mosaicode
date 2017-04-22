#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the BlockNotebook class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from blockstreeview import BlocksTreeView
from harpia.system import System as System


class BlockNotebook(Gtk.Notebook):

    """
    This class contains methods related the BlockNotebook class.
    """

    def __init__(self, main_window):
        """
        This method is the constructor.

            Parameters:
                * **main_window** (:class:`MainWindow<harpia.GUI.mainwindow>`)
        """
        Gtk.Notebook.__init__(self)
        self.tabs = []
        self.main_window = main_window
        self.set_scrollable(True)
        self.update()

    # ----------------------------------------------------------------------
    def update(self):
        languages = []

        while self.get_n_pages() > 0:
            self.remove_page(0)

        System()
        for x in System.plugins:
            instance = System.plugins[x]
            name = instance.language
            name += "/" + instance.framework
            if name in languages:
                continue
            languages.append(name)

        for language in languages:
            treeview = BlocksTreeView(self.main_window, language)
            self.append_page(treeview, Gtk.Label(language))
        self.show_all()

    # ----------------------------------------------------------------------
    def search(self, query):
        """
        This method search for a plugin.

            Returns:
                * **Types** (:class:`list<list>`)
        """
        for blocks_tree_view in self.tabs:
            blocks_tree_view.search(query)

    # ----------------------------------------------------------------------
    def get_selected_block(self):
        current_tab = None
        if self.get_current_page() > -1:
            current_tab = self.get_nth_page(self.get_current_page())
        if current_tab is None:
            return None
        return current_tab.get_selected_block()
# ----------------------------------------------------------------------
