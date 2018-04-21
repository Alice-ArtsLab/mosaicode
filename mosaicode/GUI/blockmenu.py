#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains the BlockMenu class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class BlockMenu(Gtk.Menu):
    """
    This class contains methods related the BlockMenu class
    """

    # ----------------------------------------------------------------------
    def __init__(self):
        """
        This method show the block menu.

            Parameters:
                * **block**
                * **event**
        """
        Gtk.Menu.__init__(self)
        self.block = None
        menu_item = Gtk.MenuItem("Delete")
        menu_item.connect("activate", self.__delete_clicked)
        self.append(menu_item)

        menu_item = Gtk.MenuItem("Collapse")
        menu_item.connect("activate", self.__collapse_clicked)
        self.append(menu_item)

    # ----------------------------------------------------------------------
    def show_block_menu(self, block, event):
        self.block = block

        # Shows the menu
        self.show_all()
        self.popup(None, None, None, None, event.button, event.time)

    # ----------------------------------------------------------------------
    def __delete_clicked(self, *args):
        """
        This method monitors if the button delete was clicked.

            Parameters:
            * **args**

        """
        self.block.delete()
        
    # ----------------------------------------------------------------------
    def __collapse_clicked(self, *args):
        """
        This method monitors if the button delete was clicked.

            Parameters:
            * **args**

        """
        self.block.is_collapsed = not self.block.is_collapsed
        self.block.diagram.update_flows()
