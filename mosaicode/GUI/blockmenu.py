#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains the BlockMenu class.
"""
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

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
        self.delete_menu_item = Gtk.MenuItem.new_with_label("Delete")
        self.delete_menu_item.connect("activate", self.__delete_clicked)
        self.append(self.delete_menu_item)

        self.collapse_menu_item = Gtk.MenuItem.new_with_label("Collapse")
        self.collapse_menu_item.connect("activate", self.__collapse_clicked)
        self.append(self.collapse_menu_item)

    # ----------------------------------------------------------------------
    def show(self, block, event):
        self.block = block
        self.show_all()
        self.popup_at_widget(
                    block.diagram,
                    Gdk.Gravity.CENTER, # widget_anchor
                    Gdk.Gravity.CENTER, # menu_anchor
                    event)

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
