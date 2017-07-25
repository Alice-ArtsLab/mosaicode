#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa: E402
"""
This module contains the BlockCodeEditor class.
"""
import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')
from gi.repository import Gtk
from gi.repository import GtkSource
from mosaicode.GUI.blocknotebook import BlockNotebook
from mosaicomponents.codefield import CodeField
from mosaicomponents.colorfield import ColorField
from mosaicomponents.combofield import ComboField
from mosaicomponents.commentfield import CommentField
from mosaicomponents.openfilefield import OpenFileField
from mosaicomponents.stringfield import StringField
from mosaicode.GUI.dialog import Dialog
from mosaicode.GUI.fieldtypes import *
from mosaicode.GUI.blockporteditor import BlockPortEditor
from mosaicode.GUI.blockpropertyeditor import BlockPropertyEditor
from mosaicode.system import System as System
import gettext

_ = gettext.gettext


class BlockCodeEditor(Gtk.ScrolledWindow):
    """
    This class contains methods related the BlockCodeEditor class
    """

    # ----------------------------------------------------------------------
    def __init__(self, block_editor, block):
        Gtk.ScrolledWindow.__init__(self)

        self.block_editor = block_editor
        self.block = block

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
        for code_value in self.block.codes:
            data = {"label": _("Code " + str(count)), "value": code_value}
            self.code_widgets.append(CodeField(data, self.__on_edit))
            self.code_notebook.append_page(self.code_widgets[count],
                        Gtk.Label(_("Code " + str(count))))
            count = count + 1

        self.show_all()

    # ----------------------------------------------------------------------
    def __on_edit(self, widget=None, data=None):
        """
        This method save the block.
            Parameters:
                * **block** (:class:`<>`)
        """
        count = 0
        for code_widget in self.code_widgets:
            self.block.codes[count] = self.code_widgets[count].get_value()
            count = count + 1

    # ----------------------------------------------------------------------
    def __populate_combos(self, button_bar):
        # clean the bar
        for widget in button_bar.get_children():
            button_bar.remove(widget)

        # Block Common Properties
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

        # Block Properties
        values = []
        for prop in self.block.get_properties():
            values.append("prop[" + prop["name"] + "]")
        values.sort()
        data = {"label": _("Block Properties"),
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
        for code_value in self.block.codes:
            i = 0
            for port in self.block.in_ports:
                value = System.ports[port["type"]].input_codes[count].replace(
                        "$port_number$", str(i))
                self.code_widgets[count].set_value(
                        self.code_widgets[count].get_value() + value)
                i += 1

            i = 0
            for port in self.block.out_ports:
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
