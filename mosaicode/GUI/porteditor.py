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
from mosaicomponents.stringfield import StringField
from mosaicomponents.combofield import ComboField
from mosaicomponents.colorfield import ColorField
from mosaicomponents.commentfield import CommentField
from mosaicomponents.codefield import CodeField
from mosaicomponents.openfilefield import OpenFileField
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.plugin import Plugin
from mosaicode.model.port import Port
from mosaicode.system import System as System
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
        self.multiple = CheckField({"label": _("Multiple")}, None)

        self.input_code_widgets = []
        self.output_code_widgets = []
        for code in Plugin().codes:
            self.input_code_widgets.append(CodeField({"label": ""}, None))
            self.output_code_widgets.append(CodeField({"label": ""}, None))

        if port is not None:
            System()
            self.type.set_value(port)
            self.language.set_value(System.ports[port].language)
            self.label.set_value(System.ports[port].label)
            self.color.set_value(System.ports[port].color)
            self.code.set_value(System.ports[port].code)
            self.multiple.set_value(System.ports[port].multiple)

            count = 0
            for code in Plugin().codes:
                self.input_code_widgets[count].set_value(
                        System.ports[port].input_codes[count])
                self.output_code_widgets[count].set_value(
                        System.ports[port].output_codes[count])
                count = count + 1

        vbox.pack_start(self.type, False, False, 1)
        vbox.pack_start(self.language, False, False, 1)
        vbox.pack_start(self.label, False, False, 1)
        vbox.pack_start(self.color, False, False, 1)
        vbox.pack_start(self.multiple, False, False, 1)

        self.code_notebook = Gtk.Notebook()
        self.code_notebook.set_scrollable(True)
        vbox.pack_start(self.code_notebook, True, True, 1)
        self.code_notebook.append_page(self.code, Gtk.Label(_("Connection Code")))

        count = 0
        for code_widget in self.input_code_widgets:
            self.code_notebook.append_page(code_widget, Gtk.Label(_("Input Code " + \
                    str(count))))
            count = count + 1

        count = 0
        for code_widget in self.output_code_widgets:
            self.code_notebook.append_page(code_widget, Gtk.Label(_("Output Code " + \
                    str(count))))
            count = count + 1

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

        count = 0
        for code_widget in self.input_code_widgets:
            port.input_codes[count] = self.input_code_widgets[count].get_value()
            port.output_codes[count] = self.output_code_widgets[count].get_value()
            count = count + 1

        self.port_manager.add_port(port)

# ----------------------------------------------------------------------
