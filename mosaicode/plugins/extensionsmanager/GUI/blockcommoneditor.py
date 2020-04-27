#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa: E402
"""
This module contains the BlockCommonEditor class.
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
from mosaicode.GUI.fieldtypes import *
from mosaicode.plugins.extensionsmanager.GUI.blockporteditor import BlockPortEditor
from mosaicode.plugins.extensionsmanager.GUI.blockpropertyeditor import BlockPropertyEditor
from mosaicode.system import *
import gettext

_ = gettext.gettext


class BlockCommonEditor(Gtk.ScrolledWindow):
    """
    This class contains methods related the BlockCommonEditor class
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

        data = {"label": _("Label"), "value": block.label}
        self.label_field = StringField(data, self.__on_edit)

        data = {"label": _("Language"), "value": block.language}
        self.language_field = StringField(data, self.__on_edit)

        data = {"label": _("extension"), "value": block.extension}
        self.extension_field = StringField(data, self.__on_edit)

        data = {"label": _("Block Type"), "value": block.type}
        self.type_field = StringField(data, self.__on_edit)

        data = {"label": _("Group"), "value": block.group}
        self.group_field = StringField(data, self.__on_edit)

        data = {"label": _("Color"), "value": block.get_color()}
        self.color_field = ColorField(data, self.__on_edit)
        self.color_field.set_parent_window(self.block_editor)

        data = {"label": _("Help"), "value": block.help}
        self.help_field = CommentField(data, self.__on_edit)

        vbox.pack_start(self.label_field, False, False, 1)
        vbox.pack_start(self.language_field, False, False, 1)
        vbox.pack_start(self.extension_field, False, False, 1)
        vbox.pack_start(self.type_field, False, False, 1)
        vbox.pack_start(self.group_field, False, False, 1)
        vbox.pack_start(self.color_field, False, False, 1)
        vbox.pack_start(self.help_field, False, False, 1)

        self.show_all()

    # ----------------------------------------------------------------------
    def __on_edit(self, widget=None, data=None):
        self.type_field.set_value("mosaicode.extensions." + \
                self.language_field.get_value().lower() + "." + \
                self.extension_field.get_value().lower() + "." + \
                self.label_field.get_value().lower().replace(" ","")
                )

        self.block.type = self.type_field.get_value()
        self.block.language = self.language_field.get_value()
        self.block.extension = self.extension_field.get_value()

        self.block.label = self.label_field.get_value()
        self.block.group = self.group_field.get_value()
        self.block.color = self.color_field.get_value()
        self.block.help = self.help_field.get_value()

# ----------------------------------------------------------------------
