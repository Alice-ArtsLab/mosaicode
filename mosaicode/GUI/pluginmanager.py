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
from mosaicode.GUI.components.stringfield import StringField
from mosaicode.GUI.components.combofield import ComboField
from mosaicode.GUI.components.colorfield import ColorField
from mosaicode.GUI.components.commentfield import CommentField
from mosaicode.GUI.components.codefield import CodeField
from mosaicode.GUI.components.openfilefield import OpenFileField
from mosaicode.GUI.blocknotebook import BlockNotebook
from mosaicode.GUI.fieldtypes import *
from mosaicode.GUI.plugineditor import PluginEditor
from mosaicode.GUI.dialog import Dialog
from mosaicode.model.plugin import Plugin
from mosaicode.system import System as System
import gettext

_ = gettext.gettext


class PluginManager(Gtk.Dialog):
    """
    This class contains methods related the PluginManager class
    """

    # ----------------------------------------------------------------------
    def __init__(self, main_window):
        Gtk.Dialog.__init__(self, _("Plugin Manager"), main_window, 0, ())

        self.main_window = main_window
        self.plugin = Plugin()
        self.main_control = self
        self.set_default_size(400, 300)
        box = self.get_content_area()
        vbox = Gtk.VBox()
        box.pack_start(vbox, True, True, 0)

        # Plugin List
        self.block_notebook = BlockNotebook(self)

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

        vbox.pack_start(self.block_notebook, True, True, 0)
        vbox.pack_start(button_bar, False, False, 0)

        self.show_all()
        self.show()

    # ----------------------------------------------------------------------
    def __new(self, widget=None, data=None):
        PluginEditor(self, Plugin())

    # ----------------------------------------------------------------------
    def __edit(self, widget=None, data=None):
        plugin = self.block_notebook.get_selected_block()
        if plugin is None:
            return
        PluginEditor(self, plugin)

    # ----------------------------------------------------------------------
    def __delete(self, widget=None, data=None):
        plugin = self.block_notebook.get_selected_block()
        if plugin is None:
            return
        dialog = Dialog().confirm_dialog(_("Are you sure?"), self)
        result = dialog.run()
        dialog.destroy()
        if result == Gtk.ResponseType.OK:
            self.main_window.main_control.delete_plugin(plugin)
            self.update()

    # ----------------------------------------------------------------------
    def set_block(self, plugin):
        """
        This method is called when a block is selected. Nothing to do here.
            Parameters:
                plugin
            Returns:
                None.
        """
        pass

    # ----------------------------------------------------------------------
    def add_block(self, plugin):
        """
        This method is called when a block is double clicked.

            Parameters:
                * **plugin** (:class:`<>`)
        """
        PluginEditor(self, self.block_notebook.get_selected_block())

    # ----------------------------------------------------------------------
    def add_plugin(self, plugin):
        self.main_window.main_control.add_plugin(plugin)

    # ----------------------------------------------------------------------
    def update(self):
        self.block_notebook.update()
# ----------------------------------------------------------------------
