#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa: E402
"""
This module contains the PluginManager class.
"""
import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')
from gi.repository import Gtk
from gi.repository import GtkSource
from harpia.GUI.components.stringfield import StringField
from harpia.GUI.components.combofield import ComboField
from harpia.GUI.components.colorfield import ColorField
from harpia.GUI.components.commentfield import CommentField
from harpia.GUI.components.codefield import CodeField
from harpia.GUI.components.openfilefield import OpenFileField
from harpia.GUI.fieldtypes import *
from harpia.GUI.porteditor import PortEditor
from harpia.model.plugin import Plugin
from harpia.system import System as System
import gettext

_ = gettext.gettext


class PortManager(Gtk.Dialog):
    """
    This class contains methods related the PortManager class
    """

    # ----------------------------------------------------------------------
    def __init__(self, main_window):
        Gtk.Dialog.__init__(self, _("Port Manager"), main_window, 0, ())

        self.main_window = main_window
        self.set_default_size(400, 300)
        box = self.get_content_area()

        vbox = Gtk.VBox()
        box.pack_start(vbox, True, True, 0)

        # Port List
        sw = Gtk.ScrolledWindow()
        self.tree_store = Gtk.TreeStore(str)
        self.tree_view = Gtk.TreeView(self.tree_store)

        col = Gtk.TreeViewColumn(_("Available Ports"))
        self.tree_view.append_column(col)
        cellrenderertext = Gtk.CellRendererText()
        col.pack_end(cellrenderertext, True)
        col.add_attribute(cellrenderertext, "text", 0)
        sw.add(self.tree_view)
        vbox.pack_start(sw, True, True, 0)

        # Button bar
        button_bar = Gtk.HBox()
        button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_NEW)
        button.connect("clicked", self.__new, None)
        button_bar.pack_start(button, False, False, 0)

        button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_EDIT)
        button.connect("clicked", self.__edit, None)
        button_bar.pack_start(button, False, False, 0)

        button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_DELETE)
        button.connect("clicked", self.__delete, None)
        button_bar.pack_start(button, False, False, 0)

        vbox.pack_start(button_bar, False, False, 0)

        self.__update()
        self.show_all()
        self.show()

    # ----------------------------------------------------------------------
    def add_port(self, port):
        self.main_window.main_control.add_port(port)
        self.__update()

    # ----------------------------------------------------------------------
    def __get_selected(self):
        treeselection = self.tree_view.get_selection()
        model, iterac = treeselection.get_selected()
        path = model.get_path(iterac)
        name = model.get_value(model.get_iter(path), 0)
        return name

    # ----------------------------------------------------------------------
    def __new(self, widget=None, data=None):
        PortEditor(self, None)

    # ----------------------------------------------------------------------
    def __edit(self, widget=None, data=None):
        PortEditor(self, self.__get_selected())

    # ----------------------------------------------------------------------
    def __delete(self, widget=None, data=None):
        self.main_window.main_control.delete_port(self.__get_selected())
        self.__update()

    # ----------------------------------------------------------------------
    def __update(self):
        System()
        self.tree_store.clear()
        for x in System.connectors:
            self.tree_store.append(None, [x])

# ----------------------------------------------------------------------
