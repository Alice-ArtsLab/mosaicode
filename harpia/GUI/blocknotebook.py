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
        self.main_window = main_window
        self.set_scrollable(True)
        # Load blocks
        languages = []
        self.tabs = []
        for x in System.plugins:
            instance = System.plugins[x]()
            name = instance.language
            name += "/" + instance.framework
            if name in languages:
                continue
            languages.append(name)
        for language in languages:
            treeview = BlocksTreeView(self.main_window, language)
            self.append_page(treeview, Gtk.Label(language))
            self.tabs.append(treeview)

    # ----------------------------------------------------------------------
    def get_current_tab(self):
        """
        This method get current diagram page.

            Returns:
                * **Types** (:class:`int<int>`) or None: Return number current page.

        """
        if self.get_current_page() > -1:
            return self.tabs[self.get_current_page()]
        else:
            return None

    # ----------------------------------------------------------------------
    def get_tabs(self):
        """
        This method return the diagram pages.

            Returns:
                * **Types** (:class:`list<list>`)
        """
        return self.tabs

    # ----------------------------------------------------------------------
    def get_selected_block(self):
        current_tab = self.get_current_tab()
        if current_tab is None:
            return
        return current_tab.get_selected_block()
# ----------------------------------------------------------------------
