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
from harpia.GUI.blocknotebook import BlockNotebook
from harpia.GUI.fieldtypes import *
from harpia.GUI.plugineditor import PluginEditor
from harpia.model.plugin import Plugin
from harpia.system import System as System
import gettext

_ = gettext.gettext


class PluginManager(Gtk.Dialog):
    """
    This class contains methods related the PluginManager class
    """

    # ----------------------------------------------------------------------
    def __init__(self, main_window):
        Gtk.Dialog.__init__(self, _("Plugin Manager"), main_window, 0, ())

        self.plugin = Plugin()
        self.main_control = self
        self.set_default_size(400, 300)
        box = self.get_content_area()
        vbox = Gtk.VBox()
        box.pack_start(vbox, True, True, 0)

        # Plugin List
        self.blocks = BlockNotebook(self)

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

        vbox.pack_start(self.blocks, True, True, 0)
        vbox.pack_start(button_bar, False, False, 0)

        self.show_all()
        self.show()

    # ----------------------------------------------------------------------
    def __new(self, widget=None, data=None):
        PluginEditor(self, Plugin())

    # ----------------------------------------------------------------------
    def __edit(self, widget=None, data=None):
        PluginEditor(self, self.blocks.get_selected_block())

    # ----------------------------------------------------------------------
    def __delete(self, widget=None, data=None):
        pass

    # ----------------------------------------------------------------------
    def set_block(self, plugin):
        """
        This method call add_block.

            Parameters:
                plugin
            Returns:
                None.
        """
        pass

    # ----------------------------------------------------------------------
    def add_block(self, plugin):
        """
        This method add a plugin.

            Parameters:
                * **plugin** (:class:`<>`)
        """
        pass
# ----------------------------------------------------------------------
