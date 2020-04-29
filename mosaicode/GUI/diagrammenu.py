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

        self.clear_menu_item = Gtk.MenuItem.new_with_label("Clear Code Template")
        self.clear_menu_item.connect("activate", self.__clear_code_template)
        self.append(self.clear_menu_item)

        self.insert_menu_item = Gtk.MenuItem.new_with_label("Insert comment")
        self.insert_menu_item.connect("activate", self.__insert_comment)
        self.append(self.insert_menu_item)

        self.append(Gtk.SeparatorMenuItem())

        self.delete_menu_item = Gtk.MenuItem.new_with_label("Delete")
        self.delete_menu_item.connect("activate", self.__delete)
        self.append(self.delete_menu_item)

        self.collapse_menu_item = Gtk.MenuItem.new_with_label("Collapse")
        self.collapse_menu_item.connect("activate", self.__collapse_clicked)
        self.append(self.collapse_menu_item)

        self.uncollapse_menu_item = Gtk.MenuItem.new_with_label("Uncollapse")
        self.uncollapse_menu_item.connect("activate", self.__uncollapse_clicked)
        self.append(self.uncollapse_menu_item)

    # ----------------------------------------------------------------------
    def show(self, diagram, event):
        self.diagram = diagram
        self.show_all()
        self.popup_at_widget(
                    diagram,
                    Gdk.Gravity.CENTER, # widget_anchor
                    Gdk.Gravity.CENTER, # menu_anchor
                    event)

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
