#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa: E402
"""
This module contains the PortEditor class.
"""
import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')
from gi.repository import Gtk
from gi.repository import GtkSource
from mosaicomponents.stringfield import StringField
from mosaicomponents.combofield import ComboField
from mosaicomponents.colorfield import ColorField
from mosaicomponents.commentfield import CommentField
from mosaicomponents.codefield import CodeField
from mosaicomponents.openfilefield import OpenFileField
from mosaicode.GUI.fieldtypes import *
from mosaicode.GUI.buttonbar import ButtonBar
from mosaicode.GUI.treeview import TreeView
from mosaicode.GUI.dialog import Dialog
from mosaicode.model.blockmodel import BlockModel
from mosaicode.model.port import Port
from mosaicode.system import *
import gettext

_ = gettext.gettext


class PortEditor(Gtk.Dialog):
    """
    This class contains methods related the PortEditor class
    """

    # ----------------------------------------------------------------------
    def __init__(self, port_manager, port_type):
        if port_type not in System.get_ports():
            return
        self.port_manager = port_manager
        self.port = System.get_ports()[port_type]
        Gtk.Dialog.__init__(
                        self,
                        title=_("Port Editor"),
                        transient_for=self.port_manager)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_buttons(Gtk.STOCK_SAVE, Gtk.ResponseType.OK)

        self.main_control = self
        self.set_default_size(800, 300)

        self.tabs = Gtk.Notebook()
        self.tabs.set_scrollable(True)
        box = self.get_content_area()
        box.pack_start(self.tabs, True, True, 0)

        # Common Properties --------------------------------------------------
        common_tab = Gtk.VBox()
        self.tabs.append_page(common_tab, Gtk.Label.new(_("Common Properties")))
        self.type = StringField({"label": _("Type")}, None)
        self.language = StringField({"label": _("Language")}, None)
        self.hint = StringField({"label": _("Hint")}, None)
        self.color = ColorField({"label": _("Color")}, None)
        self.color.set_parent_window(self)
        self.multiple = CheckField({"label": _("Multiple")}, None)
        self.var_name = StringField({"label": _("Var Name")}, None)

        if port_type is not None:
            System()
            self.type.set_value(port_type)
            self.language.set_value(self.port.language)
            self.hint.set_value(self.port.hint)
            self.color.set_value(self.port.color)
            self.multiple.set_value(self.port.multiple)
            self.var_name.set_value(self.port.var_name)

        common_tab.pack_start(self.type, False, False, 1)
        common_tab.pack_start(self.language, False, False, 1)
        common_tab.pack_start(self.hint, False, False, 1)
        common_tab.pack_start(self.color, False, False, 1)
        common_tab.pack_start(self.multiple, False, False, 1)
        common_tab.pack_start(self.var_name, False, False, 1)

        # Connection Code ----------------------------------------------------
        code_tab = Gtk.VBox()
        self.tabs.append_page(code_tab, Gtk.Label.new(_("Connection Code")))

        # Top Button bar
        top_button_bar = Gtk.HBox()
        code_tab.pack_start(top_button_bar, False, False, 1)
        self.__populate_combos(top_button_bar)

        self.code = CodeField({"label": _("Connection Code")}, None)
        code_tab.pack_start(self.code, True, True, 1)
        if port_type is not None:
            System()
            self.code.set_value(self.port.code)

        self.show_all()
        result = self.show()
        if result == Gtk.ResponseType.OK:
            self.__save()
        self.close()
        self.destroy()

    # ----------------------------------------------------------------------
    def __populate_combos(self, top_button_bar):
        # clean the bar
        for widget in top_button_bar.get_children():
            top_button_bar.remove(widget)

        # Port Common Properties
        data = {"label": _("Common Properties"),
                "name": "common",
                "values": ["$input$",
                           "$output$"]}

        self.commons = ComboField(data, self.__on_select)
        top_button_bar.pack_start(self.commons, False, False, 0)
        top_button_bar.show_all()

    # ----------------------------------------------------------------------
    def __on_select(self, widget=None, data=None):
        value = widget.get_parent().get_value()
        self.code.insert_at_cursor(value)

    # ----------------------------------------------------------------------
    def __save(self):
        port = Port()
        port.type = self.type.get_value()
        port.language = self.language.get_value()
        port.hint = self.hint.get_value()
        port.color = self.color.get_value()
        port.multiple = self.multiple.get_value()
        port.code = self.code.get_value()
        port.var_name = self.var_name.get_value()
        self.port_manager.add_port(port)

# ----------------------------------------------------------------------
