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
        Gtk.Notebook.__init__(self)


    def show_block_menu(self, block, event):
        self.block = block

        menu_item = Gtk.MenuItem("Delete")
        menu_item.connect("activate", self.__delete_clicked)
        self.append(menu_item)


        # Shows the menu
        self.show_all()
        self.popup(None, None, None, None, event.button.button, event.time)

    # ----------------------------------------------------------------------
    def __delete_clicked(self, *args):
        """
        This method monitors if the button delete was clicked.

            Parameters:
            * **args**

        """
        self.block.delete()
