#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the ExtensionsManagerMenu class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mosaicode.model.plugin import Plugin
from mosaicode.plugins.extensionsmanager.control.extensionsmanagercontrol import ExtensionsManagerControl
import gettext

_ = gettext.gettext

class ExtensionsManagerMenu(Gtk.Menu):
    """
    This class contains methods related the ExtensionsManagerMenu
    """
    # ----------------------------------------------------------------------

    def __init__(self, main_window):
        """Constructor."""
        Gtk.Menu.__init__(self)

        self.control = ExtensionsManagerControl(main_window)

        main_window.menu.create_menu(_("Code Template Manager"),
                                None, self, self.control.code_template_manager)

        main_window.menu.create_menu(_("Block Manager"), None,
                                             self, self.control.block_manager)

        main_window.menu.create_menu(_("Port Manager"), None,
                   self, self.control.port_manager)

        self.append(Gtk.SeparatorMenuItem())
        export_blocks = main_window.menu.create_menu(_("Export As..."), None, self, None)
        export_blocks_menu = Gtk.Menu()
        export_blocks.set_submenu(export_blocks_menu)
        main_window.menu.create_menu(_("XML"), None, export_blocks_menu, self.control.export_xml_dialog)
    
