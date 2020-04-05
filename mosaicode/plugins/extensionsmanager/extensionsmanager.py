#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the ExtensionsManagerMenu class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mosaicode.model.plugin import Plugin
from mosaicode.plugins.extensionsmanager.GUI.extensionsmanagermenu import ExtensionsManagerMenu
from mosaicode.plugins.extensionsmanager.GUI.blockmenuitem import BlockMenuItem

import gettext

_ = gettext.gettext

class ExtensionsManager(Plugin):
    """
    This class contains methods related the ExtensionsManagerMenu
    """

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor."""
        self.label = _("Extensions Manager")

    # ----------------------------------------------------------------------
    def load(self, main_window):
        plugin_menu = main_window.menu.plugins_menu

        item = Gtk.MenuItem()
        item.set_label(self.label)
        plugin_menu.append(item)

        sub_menu = ExtensionsManagerMenu(main_window)
        submenu_item = Gtk.MenuItem()
        submenu_item.set_label("item text")
        item.set_submenu(sub_menu)

        menu_item = BlockMenuItem(main_window)
        main_window.block_menu.append(menu_item)
