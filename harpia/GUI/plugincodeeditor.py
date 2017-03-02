#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa: E402
"""
This module contains the PluginCode class.
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
from harpia.GUI.pluginpropertyeditor import PluginPropertyEditor
from harpia.model.plugin import Plugin
from harpia.system import System as System
import gettext

_ = gettext.gettext


class PluginCodeEditor(Gtk.ScrolledWindow):
    """
    This class contains methods related the PluginCode class
    """

    # ----------------------------------------------------------------------
    def __init__(self, plugin_editor, plugin):
        Gtk.ScrolledWindow.__init__(self)

        self.plugin_editor = plugin_editor
        self.plugin = plugin

        for widget in self.get_children():
            self.remove(widget)
        vbox = Gtk.VBox()
        self.add(vbox)

        # Button bar
        button_bar = Gtk.HBox()
        data = {"label": _("Properties"), "values": ["id", "language", "framework"]}
        properties = ComboField(data, None)
        button_bar.pack_start(properties, False, False, 0)
        vbox.pack_start(button_bar, False, False, 1)

        codes = Gtk.Notebook()
        codes.set_scrollable(True)
        vbox.pack_start(codes, True, True, 1)

        data = {"label": _("Header"), "value": plugin.generate_header()}
        self.header = CodeField(data, None)
        data = {"label": _("Vars"), "value": plugin.generate_vars()}
        self.vars = CodeField(data, None)
        data = {"label": _("Function Call"), "value": plugin.generate_function_call()}
        self.function_call = CodeField(data, None)
        data = {"label": _("Dealloc"), "value": plugin.generate_dealloc()}
        self.dealloc = CodeField(data, None)
        data = {"label": _("Out Dealloc"), "value": plugin.generate_out_dealloc()}
        self.out_dealloc = CodeField(data, None)

        codes.append_page(self.header, Gtk.Label(_("Header")))
        codes.append_page(self.vars, Gtk.Label(_("Vars")))
        codes.append_page(self.function_call, Gtk.Label(_("Function Call")))
        codes.append_page(self.dealloc, Gtk.Label(_("Dealloc")))
        codes.append_page(self.out_dealloc, Gtk.Label(_("Out Dealloc")))

        self.show_all()

    # ----------------------------------------------------------------------
    def _on_edit(self, widget=None, data=None):
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

# ----------------------------------------------------------------------
