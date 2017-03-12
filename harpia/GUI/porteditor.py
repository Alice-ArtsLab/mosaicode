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
from harpia.model.port import Port
from harpia.system import System as System
import gettext

_ = gettext.gettext


class PortEditor(Gtk.Dialog):
    """
    This class contains methods related the PortEditor class
    """

    # ----------------------------------------------------------------------
    def __init__(self, port_manager, port):
        self.port_manager = port_manager
        Gtk.Dialog.__init__(self, _("Port Editor"), self.port_manager,
                            0, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        self.main_control = self
        self.set_default_size(600, 300)

        vbox = Gtk.VBox()
        box = self.get_content_area()
        box.pack_start(vbox, True, True, 0)

        self.type = StringField({"label": _("Type")}, None)
        self.language = StringField({"label": _("Language")}, None)
        self.label = StringField({"label": _("Label")}, None)
        self.color = ColorField({"label": _("Color")}, None)
        self.color.set_parent_window(self)
        self.code = CodeField({"label": _("Code")}, None)
        self.input_vars = CodeField({"label": _("Input Declaration")}, None)
        self.output_vars = CodeField({"label": _("Output Declaration")}, None)
        self.input_dealloc = CodeField({"label": _("Input Deallocation")}, None)
        self.output_dealloc = CodeField({"label": _("Output Deallocation")}, None)
        self.multiple = CheckField({"label": _("Multiple")}, None)
        if port is not None:
            System()
            self.type.set_value(port)
            self.language.set_value(System.ports[port].get_language())
            self.label.set_value(System.ports[port].get_label())
            self.color.set_value(System.ports[port].get_color())
            self.code.set_value(System.ports[port].get_code())
            self.input_vars.set_value(System.ports[port].get_input_vars())
            self.output_vars.set_value(System.ports[port].get_output_vars())
            self.input_dealloc.set_value(System.ports[port].get_input_dealloc())
            self.output_dealloc.set_value(System.ports[port].get_output_dealloc())
            self.multiple.set_value(System.ports[port].get_multiple())

        vbox.pack_start(self.type, False, False, 1)
        vbox.pack_start(self.language, False, False, 1)
        vbox.pack_start(self.label, False, False, 1)
        vbox.pack_start(self.color, False, False, 1)
        vbox.pack_start(self.multiple, False, False, 1)

        self.codes = Gtk.Notebook()
        self.codes.set_scrollable(True)
        vbox.pack_start(self.codes, True, True, 1)

        self.codes.append_page(self.code, Gtk.Label(_("Connection Code")))
        self.codes.append_page(self.input_vars, Gtk.Label(_("Input Vars")))
        self.codes.append_page(self.output_vars, Gtk.Label(_("Outpur Vars")))
        self.codes.append_page(self.input_dealloc, Gtk.Label(_("Input Dealloc")))
        self.codes.append_page(self.output_dealloc, Gtk.Label(_("Output Dealloc")))

        self.show_all()
        result = self.run()
        if result == Gtk.ResponseType.OK:
            self.__save()
        self.close()
        self.destroy()

    # ----------------------------------------------------------------------
    def __save(self):
        port = Port()
        port.type = self.type.get_value()
        port.language = self.language.get_value()
        port.label = self.label.get_value()
        port.color = self.color.get_value()
        port.multiple = self.multiple.get_value()
        port.code = self.code.get_value()
        port.input_vars = self.input_vars.get_value()
        port.output_vars = self.output_vars.get_value()
        port.input_dealloc = self.input_dealloc.get_value()
        port.output_dealloc = self.output_dealloc.get_value()
        self.port_manager.add_port(port)

# ----------------------------------------------------------------------
