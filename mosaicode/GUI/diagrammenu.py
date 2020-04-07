#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains the BlockMenu class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mosaicode.control.diagramcontrol import DiagramControl

class DiagramMenu(Gtk.Menu):
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
        self.diagram = None
        self.x = 0
        self.y = 0

        menu_item = Gtk.MenuItem("Clear Code Template")
        menu_item.connect("activate", self.__clear_code_template)
        self.append(menu_item)

        menu_item = Gtk.MenuItem("Insert comment")
        menu_item.connect("activate", self.__insert_comment)
        self.append(menu_item)

        self.append(Gtk.SeparatorMenuItem())

        menu_item = Gtk.MenuItem("Delete")
        menu_item.connect("activate", self.__delete)
        self.append(menu_item)

        menu_item = Gtk.MenuItem("Collapse")
        menu_item.connect("activate", self.__collapse_clicked)
        self.append(menu_item)

        menu_item = Gtk.MenuItem("Uncollapse")
        menu_item.connect("activate", self.__uncollapse_clicked)
        self.append(menu_item)

    # ----------------------------------------------------------------------
    def show(self, diagram, event):
        self.diagram = diagram
        self.x = event.x
        self.y = event.y
        self.show_all()
        self.popup(None, None, None, None, event.button, event.time)

    # ----------------------------------------------------------------------
    def __clear_code_template(self, *args):
        """
        This method monitors if the button delete was clicked.

            Parameters:
            * **args**

        """
        self.diagram.code_template = None
    # ----------------------------------------------------------------------
    def __insert_comment(self, *args):
        """
        This method monitors if the button delete was clicked.

            Parameters:
            * **args**

        """
        comment = DiagramControl(self.diagram).add_comment()
        comment.move(int(float(self.x)), int(float(self.y)))
    # ----------------------------------------------------------------------
    def __delete(self, *args):
        """
        This method monitors if the button delete was clicked.

            Parameters:
            * **args**

        """
        self.diagram.delete()

    # ----------------------------------------------------------------------
    def __uncollapse_clicked(self, *args):
        """
        This method monitors if the button delete was clicked.

            Parameters:
            * **args**

        """
        self.diagram.collapse(False)
    # ----------------------------------------------------------------------
    def __collapse_clicked(self, *args):
        """
        This method monitors if the button delete was clicked.

            Parameters:
            * **args**

        """
        self.diagram.collapse(True)
