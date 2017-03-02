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
from harpia.GUI.blocknotebook import BlockNotebook
from harpia.GUI.components.codefield import CodeField
from harpia.GUI.components.colorfield import ColorField
from harpia.GUI.components.combofield import ComboField
from harpia.GUI.components.commentfield import CommentField
from harpia.GUI.components.openfilefield import OpenFileField
from harpia.GUI.components.stringfield import StringField
from harpia.GUI.dialog import Dialog
from harpia.GUI.fieldtypes import *
from harpia.GUI.pluginporteditor import PluginPortEditor
from harpia.GUI.plugincommoneditor import PluginCommonEditor
from harpia.GUI.pluginpropertyeditor import PluginPropertyEditor
from harpia.model.plugin import Plugin
from harpia.system import System as System
import gettext

_ = gettext.gettext


class PluginEditor(Gtk.Dialog):
    """
    This class contains methods related the PluginManager class
    """

    # ----------------------------------------------------------------------
    def __init__(self, plugin_manager, plugin):
        Gtk.Dialog.__init__(self, _("Plugin Editor"),
                            plugin_manager,
                            0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        self.plugin_manager = plugin_manager
        self.plugin = plugin
        self.main_control = self
        self.set_default_size(800, 600)
        box = self.get_content_area()

        self.tabs = Gtk.Notebook()
        self.tabs.set_scrollable(True)
        box.pack_start(self.tabs, True, True, 0)

        self.tabs.append_page(PluginCommonEditor(self, self.plugin),
                    Gtk.Label(_("Common Properties")))
        self.tabs.append_page(PluginPropertyEditor(self, self.plugin),
                    Gtk.Label(_("Properties")))
        self.tabs.append_page(PluginPortEditor(self, self.plugin),
                    Gtk.Label(_("Ports")))

        # ----------------------------------------------------------------------
        # Code section
        # ----------------------------------------------------------------------
        self.code = Gtk.ScrolledWindow()
        self.code.set_shadow_type(Gtk.ShadowType.IN)
        self.tabs.append_page(self.code, Gtk.Label(_("Code")))
        self.__create_code_tab()

        self.show_all()
        self.__set_plugin(plugin)
        result = self.run()
        if result == Gtk.ResponseType.OK:
            self.__save()
        self.close()
        self.destroy()

    # ----------------------------------------------------------------------
    def __create_code_tab(self):
        for widget in self.code.get_children():
            self.code.remove(widget)
        vbox = Gtk.VBox()
        self.code.add(vbox)

        # Button bar
        button_bar = Gtk.HBox()
        data = {"label": _("Properties"), "values": ["id", "language", "framework"]}
        properties = ComboField(data, None)
        button_bar.pack_start(properties, False, False, 0)
        vbox.pack_start(button_bar, False, False, 1)

        codes = Gtk.Notebook()
        codes.set_scrollable(True)
        vbox.pack_start(codes, True, True, 1)

        self.header = CodeField({"label": _("Header")}, None)
        self.vars = CodeField({"label": _("Vars")}, None)
        self.function_call = CodeField({"label": _("Function Call")}, None)
        self.dealloc = CodeField({"label": _("Dealloc")}, None)
        self.out_dealloc = CodeField({"label": _("Out Dealloc")}, None)

        codes.append_page(self.header, Gtk.Label(_("Header")))
        codes.append_page(self.vars, Gtk.Label(_("Vars")))
        codes.append_page(self.function_call, Gtk.Label(_("Function Call")))
        codes.append_page(self.dealloc, Gtk.Label(_("Dealloc")))
        codes.append_page(self.out_dealloc, Gtk.Label(_("Out Dealloc")))

    # ----------------------------------------------------------------------
    def __set_plugin(self, plugin):
        """
        This method add a plugin.

            Parameters:
                * **plugin** (:class:`<>`)
        """

        self.header.set_value(plugin.generate_header())
        self.vars.set_value(plugin.generate_vars())
        self.function_call.set_value(plugin.generate_function_call())
        self.dealloc.set_value(plugin.generate_dealloc())
        self.out_dealloc.set_value(plugin.generate_out_dealloc())

    # ----------------------------------------------------------------------
    def __save(self):
        """
        This method save the plugin.
            Parameters:
                * **plugin** (:class:`<>`)
        """

        self.plugin.header = self.header.get_value()
        self.plugin.vars = self.vars.get_value()
        self.plugin.function_call = self.function_call.get_value()
        self.plugin.dealloc = self.dealloc.get_value()
        self.plugin.out_dealloc = self.out_dealloc.get_value()
        self.plugin_manager.add_plugin(self.plugin)

# ----------------------------------------------------------------------
