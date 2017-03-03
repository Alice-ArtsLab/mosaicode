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
from harpia.GUI.pluginpropertyeditor import PluginPropertyEditor
from harpia.model.plugin import Plugin
from harpia.system import System as System
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

        data = {"label": _("Label"), "value": plugin.get_label()}
        self.label_field = StringField(data, self._on_edit)

        data = {"label": _("Language"), "value": plugin.get_language()}
        self.language_field = StringField(data, self._on_edit)

        data = {"label": _("Framework"), "value": plugin.get_framework()}
        self.framework_field = StringField(data, self._on_edit)

        data = {"label": _("Plugin Type"), "value": plugin.get_type()}
        self.type_field = StringField(data, self._on_edit)

        data = {"label": _("Group"), "value": plugin.get_group()}
        self.group_field = StringField(data, self._on_edit)

        data = {"label": _("Color"), "value": plugin.get_color()}
        self.color_field = ColorField(data, self._on_edit)
        self.color_field.set_parent_window(self.plugin_editor)

        data = {"label": _("Help"), "value": plugin.get_help()}
        self.help_field = CommentField(data, self._on_edit)

        vbox.pack_start(self.label_field, False, False, 1)
        vbox.pack_start(self.language_field, False, False, 1)
        vbox.pack_start(self.framework_field, False, False, 1)
        vbox.pack_start(self.type_field, False, False, 1)
        vbox.pack_start(self.group_field, False, False, 1)
        vbox.pack_start(self.color_field, False, False, 1)
        vbox.pack_start(self.help_field, False, False, 1)

        self.show_all()

    # ----------------------------------------------------------------------
    def _on_edit(self, widget=None, data=None):
        self.type_field.set_value("harpia.plugins." + \
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
