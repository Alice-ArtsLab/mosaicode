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
from mosaicode.GUI.plugincommoneditor import PluginCommonEditor
from mosaicode.GUI.pluginpropertyeditor import PluginPropertyEditor
from mosaicode.GUI.plugincodeeditor import PluginCodeEditor
from mosaicode.model.plugin import Plugin
from mosaicode.system import System as System
import gettext

_ = gettext.gettext


class PluginEditor(Gtk.Dialog):
    """
    This class contains methods related the PluginManager class
    """

    # ----------------------------------------------------------------------
    def __init__(self, plugin_manager, plugin):
        Gtk.Dialog.__init__(self, _("Plugin Editor"),
                            plugin_manager,
                            0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        self.plugin_manager = plugin_manager
        self.plugin = plugin
        self.set_default_size(800, 600)
        box = self.get_content_area()

        self.tabs = Gtk.Notebook()
        self.tabs.set_scrollable(True)
        box.pack_start(self.tabs, True, True, 0)

        self.tabs.append_page(PluginCommonEditor(self, self.plugin),
                    Gtk.Label(_("Common Properties")))
        self.tabs.append_page(PluginPropertyEditor(self, self.plugin),
                    Gtk.Label(_("Properties")))
        self.tabs.append_page(PluginPortEditor(self, self.plugin),
                    Gtk.Label(_("Ports")))
        self.tabs.append_page(PluginCodeEditor(self, self.plugin),
                    Gtk.Label(_("Code")))

        self.show_all()
        result = self.run()
        if result == Gtk.ResponseType.OK:
            self.plugin_manager.main_control.add_plugin(plugin)
            self.plugin_manager.update()
        self.close()
        self.destroy()

# ----------------------------------------------------------------------
