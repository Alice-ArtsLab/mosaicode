#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the PreferenceWindow class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mosaicode.system import System as System
from mosaicomponents.stringfield import StringField
from mosaicomponents.openfilefield import OpenFileField
from mosaicomponents.intfield import IntField
import gettext

_ = gettext.gettext


class PreferenceWindow(Gtk.Dialog):
    """
    This class contains methods related the PreferenceWindow class
    """

    def __init__(self, main_window):
        """
        This method is the constructor.
        """
        Gtk.Dialog.__init__(self, _("Preferences"), main_window,
                            0, (Gtk.STOCK_CANCEL,
                                Gtk.ResponseType.CANCEL,
                                Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.main_window = main_window
        self.properties = System.properties
        box = self.get_content_area()
        box.set_border_width(3)

        self.tabs = Gtk.Notebook()
        box.add(self.tabs)

        # Default directory
        # ----------------------------------------------------------------------
        self.default_directory_tab = Gtk.Box()
        self.default_directory_tab.set_border_width(10)
        self.tabs.append_page(self.default_directory_tab, Gtk.Label(_("Default Directory")))
        self.__create_default_directory_tab()

        # Grid Preferences
        # ----------------------------------------------------------------------
        self.grid_preferences_tab = Gtk.Box()
        self.grid_preferences_tab.set_border_width(10)
        self.tabs.append_page(self.grid_preferences_tab, Gtk.Label(_("Grid Preferences")))
        self.__create_grid_preferences_tab()

        # Network Preferences
        # ----------------------------------------------------------------------
        self.network_preferences_tab = Gtk.Box()
        self.network_preferences_tab.set_border_width(10)
        self.tabs.append_page(self.network_preferences_tab, Gtk.Label(_("Network Preferences")))
        self.__create_network_preferences_tab()

        self.show_all()

    # ----------------------------------------------------------------------
    def run(self):
        response = Gtk.Dialog.run(self)

        if response == Gtk.ResponseType.OK:
            self.properties.default_directory = self.default_directory.get_value()
            self.properties.default_filename = self.default_filename.get_value()
            self.properties.grid = self.grid.get_value()
            self.properties.port = self.port.get_value()
            self.main_window.main_control.redraw(None)

        self.close()
        self.destroy()

    # Default directory
    # ----------------------------------------------------------------------
    def __create_default_directory_tab(self):
        vbox = Gtk.VBox()
        self.default_directory_tab.add(vbox)

        data = {"label": _("Default directory:"),
                "value": self.properties.default_directory}
        self.default_directory = OpenFileField(data, None)
        vbox.add(self.default_directory)

        # Default directory
        data = {"label": _("Default Filename:"),
                "value": self.properties.default_filename}
        self.default_filename = StringField(data, None)
        vbox.add(self.default_filename)

        vbox.add(Gtk.Label(_("\nName Wildcards:\n" +
                             "\t%d = Date | %n = diagram name |"
                             " %t = time value | %l = language\n")))

        self.default_directory_tab.show_all()

    # Grid Preferences
    # ----------------------------------------------------------------------
    def __create_grid_preferences_tab(self):
        vbox = Gtk.VBox()
        self.grid_preferences_tab.add(vbox)

        data = {"label": _("Grid size"), "value": self.properties.grid}
        self.grid = IntField(data, None)
        vbox.add(self.grid)

        self.grid_preferences_tab.show_all()

    # ----------------------------------------------------------------------
    def __create_network_preferences_tab(self):
        """Creates the networks preferences tab."""
        vbox = Gtk.VBox()
        self.network_preferences_tab.add(vbox)

        data = {"label": _("Web Server Port"), "value": self.properties.port, "lower": 1024, "upper": 49151}
        self.port = IntField(data, None)
        vbox.add(self.port)

        self.network_preferences_tab.show_all()

