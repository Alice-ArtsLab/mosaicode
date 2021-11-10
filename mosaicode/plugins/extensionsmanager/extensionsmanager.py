#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the ExtensionsManagerMenu class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mosaicode.plugins.extensionsmanager.codetemplatemanager import CodeTemplateManager
from mosaicode.plugins.extensionsmanager.blockmanager import BlockManager
from mosaicode.plugins.extensionsmanager.portmanager import PortManager
from mosaicode.control.portcontrol import PortControl
from mosaicode.control.blockcontrol import BlockControl
from mosaicode.control.codetemplatecontrol import CodeTemplateControl
import gettext

_ = gettext.gettext

class ExtensionsManager(Gtk.Menu):
    """
    This class contains methods related the ExtensionsManagerMenu
    """

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor."""
        Gtk.Menu.__init__(self)
        self.label = _("Extensions Manager")

    # ----------------------------------------------------------------------
    def load(self, main_window):

        self.main_window = main_window
        main_window.menu.create_menu(
                _("Code Template Manager"),
                None,
                self,
                self.__show_code_template_manager
                )

        main_window.menu.create_menu(
                _("Block Manager"),
                None,
                self,
                self.__show_block_manager
                )

        main_window.menu.create_menu(
                _("Port Manager"),
                None,
                self,
                self.__show_port_manager
                )

        main_window.menu.create_menu(
                _("Export all Extensions"),
                None,
                self,
                self.__export
                )

        main_window.menu.create_menu(
                _("Import Extension"),
                None,
                self,
                self.__import
                )

        item = Gtk.MenuItem()
        item.set_label(self.label)
        main_window.menu.append(item)
        item.set_submenu(self)

    # ----------------------------------------------------------------------
    def __show_code_template_manager(self):
        """
        This add a new Code Template.
        """
        CodeTemplateManager(self.main_window)

    # ----------------------------------------------------------------------
    def __show_block_manager(self):
        """
        This add a new Block.
        """
        BlockManager(self.main_window)

    # ----------------------------------------------------------------------
    def __show_port_manager(self):
        """
        This add a new port.
        """
        PortManager(self.main_window)
        
    # ----------------------------------------------------------------------
    def __export(self):
        """
        Export all data.
        """
        self.main_window.main_control.export_extensions()

    # ----------------------------------------------------------------------
    def __import(self):
        """
        Export all data.
        """
        self.main_window.main_control.import_extensions()
