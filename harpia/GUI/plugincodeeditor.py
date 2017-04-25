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
        vbox.pack_start(button_bar, False, False, 1)
        self.__populate_combos(button_bar)

        self.code_notebook = Gtk.Notebook()
        self.code_notebook.set_scrollable(True)
        vbox.pack_start(self.code_notebook, True, True, 1)

        self.code_widgets = []
        count = 0
        for code_value in self.plugin.codes:
            data = {"label": _("Code " + str(count)), "value": code_value}
            self.code_widgets.append(CodeField(data, self.__on_edit))
            self.code_notebook.append_page(self.code_widgets[count],
                        Gtk.Label(_("Code " + str(count))))
            count = count + 1

        self.show_all()

    # ----------------------------------------------------------------------
    def __on_edit(self, widget=None, data=None):
        """
        This method save the plugin.
            Parameters:
                * **plugin** (:class:`<>`)
        """
        count = 0
        for code_widget in self.code_widgets:
            self.plugin.codes[count] = self.code_widgets[count].get_value()
            count = count + 1

    # ----------------------------------------------------------------------
    def __populate_combos(self, button_bar):
        # clean the bar
        for widget in button_bar.get_children():
            button_bar.remove(widget)

        # Plugin Common Properties
        data = {"label": _("Common Properties"),
                "name": "common",
                "values": ["id",
                           "label",
                           "x",
                           "y",
                           "type",
                           "language",
                           "framework",
                           "group",
                           "color",
                           "help"]}
        self.commons = ComboField(data, self.__on_select)
        button_bar.pack_start(self.commons, False, False, 0)

        # Plugin Properties
        values = []
        for prop in self.plugin.get_properties():
            values.append("prop[" + prop["name"] + "]")
        values.sort()
        data = {"label": _("Plugin Properties"),
                "name":"props",
                "values": values}
        self.props = ComboField(data, self.__on_select)
        button_bar.pack_start(self.props, False, False, 0)

        # Refresh Button
        button = Gtk.Button.new_with_label("Refresh")
        button.connect("clicked", self.__refresh, button_bar)
        button_bar.pack_start(button, False, False, 0)

        # Generate Default Code Button
        button = Gtk.Button.new_with_label("Generate Default Code")
        button.connect("clicked", self.__generate_default, None)
        button_bar.pack_start(button, False, False, 0)
        
        button_bar.show_all()

    # ----------------------------------------------------------------------
    def __refresh(self, widget, button_bar):
        """
        This method monitors if the button was clicked.

            Parameters:

        """
        self.__populate_combos(button_bar)

    # ----------------------------------------------------------------------
    def __generate_default(self, widget, button_bar):
        """
        This method monitors if the button was clicked.

            Parameters:
        """
        count = 0
        for code_value in self.plugin.codes:
            i = 0
            for port in self.plugin.in_ports:
                value = System.ports[port["type"]].input_codes[count].replace(
                        "$port_number$", str(i))
                self.code_widgets[count].set_value(
                        self.code_widgets[count].get_value() + value)
                i += 1

            i = 0
            for port in self.plugin.out_ports:
                value = System.ports[port["type"]].output_codes[count].replace(
                        "$port_number$", str(i))
                self.code_widgets[count].set_value(
                        self.code_widgets[count].get_value() + value)
                i += 1

            count = count + 1

    # ----------------------------------------------------------------------
    def __get_current_code_area(self):
        current_tab = self.code_notebook.get_nth_page(self.code_notebook.get_current_page())
        return current_tab

    # ----------------------------------------------------------------------
    def __on_select(self, widget=None, data=None):
        code_area = self.__get_current_code_area()
        value = widget.get_parent().get_value()
        code_area.insert_at_cursor("$" + value + "$")
# ----------------------------------------------------------------------
