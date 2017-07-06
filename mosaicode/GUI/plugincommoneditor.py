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
from mosaicode.GUI.blocknotebook import BlockNotebook
from mosaicomponents.codefield import CodeField
from mosaicomponents.colorfield import ColorField
from mosaicomponents.combofield import ComboField
from mosaicomponents.commentfield import CommentField
from mosaicomponents.openfilefield import OpenFileField
from mosaicomponents.stringfield import StringField
from mosaicode.GUI.dialog import Dialog
from mosaicode.GUI.fieldtypes import *
from mosaicode.GUI.pluginporteditor import PluginPortEditor
from mosaicode.GUI.pluginpropertyeditor import PluginPropertyEditor
from mosaicode.model.plugin import Plugin
from mosaicode.system import System as System
import gettext

_ = gettext.gettext


class PluginCommonEditor(Gtk.ScrolledWindow):
    """
    This class contains methods related the PluginManager class
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

        data = {"label": _("Label"), "value": plugin.label}
        self.label_field = StringField(data, self.__on_edit)

        data = {"label": _("Language"), "value": plugin.language}
        self.language_field = StringField(data, self.__on_edit)

        data = {"label": _("Framework"), "value": plugin.framework}
        self.framework_field = StringField(data, self.__on_edit)

        data = {"label": _("Plugin Type"), "value": plugin.type}
        self.type_field = StringField(data, self.__on_edit)

        data = {"label": _("Group"), "value": plugin.group}
        self.group_field = StringField(data, self.__on_edit)

        data = {"label": _("Color"), "value": plugin.get_color()}
        self.color_field = ColorField(data, self.__on_edit)
        self.color_field.set_parent_window(self.plugin_editor)

        data = {"label": _("Help"), "value": plugin.help}
        self.help_field = CommentField(data, self.__on_edit)

        vbox.pack_start(self.label_field, False, False, 1)
        vbox.pack_start(self.language_field, False, False, 1)
        vbox.pack_start(self.framework_field, False, False, 1)
        vbox.pack_start(self.type_field, False, False, 1)
        vbox.pack_start(self.group_field, False, False, 1)
        vbox.pack_start(self.color_field, False, False, 1)
        vbox.pack_start(self.help_field, False, False, 1)

        self.show_all()

    # ----------------------------------------------------------------------
    def __on_edit(self, widget=None, data=None):
        self.type_field.set_value("mosaicode.extensions." + \
                self.language_field.get_value().lower() + "." + \
                self.framework_field.get_value().lower() + "." + \
                self.label_field.get_value().lower().replace(" ","")
                )

        self.plugin.type = self.type_field.get_value()
        self.plugin.language = self.language_field.get_value()
        self.plugin.framework = self.framework_field.get_value()

        self.plugin.label = self.label_field.get_value()
        self.plugin.group = self.group_field.get_value()
        self.plugin.color = self.color_field.get_value()
        self.plugin.help = self.help_field.get_value()

# ----------------------------------------------------------------------
