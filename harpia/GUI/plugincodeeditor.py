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

        self.codes = Gtk.Notebook()
        self.codes.set_scrollable(True)
        vbox.pack_start(self.codes, True, True, 1)

        data = {"label": _("Header"), "value": plugin.generate_header()}
        self.header = CodeField(data, self.__on_edit)
        data = {"label": _("Vars"), "value": plugin.generate_vars()}
        self.vars = CodeField(data, self.__on_edit)
        data = {"label": _("Function Call"), "value": plugin.generate_function_call()}
        self.function_call = CodeField(data, self.__on_edit)
        data = {"label": _("Dealloc"), "value": plugin.generate_dealloc()}
        self.dealloc = CodeField(data, self.__on_edit)
        data = {"label": _("Out Dealloc"), "value": plugin.generate_out_dealloc()}
        self.out_dealloc = CodeField(data, self.__on_edit)

        self.codes.append_page(self.header, Gtk.Label(_("Header")))
        self.codes.append_page(self.vars, Gtk.Label(_("Vars")))
        self.codes.append_page(self.function_call, Gtk.Label(_("Function Call")))
        self.codes.append_page(self.dealloc, Gtk.Label(_("Dealloc")))
        self.codes.append_page(self.out_dealloc, Gtk.Label(_("Out Dealloc")))

        self.show_all()

    # ----------------------------------------------------------------------
    def __on_edit(self, widget=None, data=None):
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
        self.vars.set_value(self.vars.get_value() + \
            "// --------------- Generated dafault Code ---------")
        self.dealloc.set_value(self.dealloc.get_value() + \
            "// --------------- Generated dafault Code ---------")
        i = 0
        for port in self.plugin.get_in_ports():
            value = System.ports[port["type"]].input_vars.replace("$port_number$", str(i))
            self.vars.set_value(self.vars.get_value() + value)
            value = System.ports[port["type"]].input_dealloc.replace("$port_number$", str(i))
            self.dealloc.set_value(self.dealloc.get_value() + value)
            i += 1

        i = 0
        for port in self.plugin.get_out_ports():
            value = System.ports[port["type"]].output_vars.replace("$port_number$", str(i))
            self.vars.set_value(self.vars.get_value() + value)
            value = System.ports[port["type"]].output_dealloc.replace("$port_number$", str(i))
            self.dealloc.set_value(self.dealloc.get_value() + value)
            i += 1

        self.vars.set_value(self.vars.get_value() + \
            "// --------------- End of Generated dafault Code ---------\n")
        self.dealloc.set_value(self.dealloc.get_value() + \
            "// --------------- End of Generated dafault Code ---------\n")

    # ----------------------------------------------------------------------
    def __get_current_code_area(self):
        current_tab = self.codes.get_nth_page(self.codes.get_current_page())
        return current_tab

    # ----------------------------------------------------------------------
    def __on_select(self, widget=None, data=None):
        code_area = self.__get_current_code_area()
        value = widget.get_parent().get_value()
        code_area.set_value(code_area.get_value() + "$" + value + "$")
# ----------------------------------------------------------------------
