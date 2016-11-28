#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the PreferenceWindow class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from harpia.system import System as System
from harpia.GUI.components.stringfield import StringField
from harpia.GUI.components.openfilefield import OpenFileField
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
        Gtk.Dialog.__init__(self, _("Code Window"), main_window,
                            0, (Gtk.STOCK_CANCEL,
                                Gtk.ResponseType.CANCEL,
                                Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.properties = System.properties
        box = self.get_content_area()
        vbox = Gtk.VBox()
        box.add(vbox)

        # Default directory
        data = {"label": _("Default directory"),
                "value": self.properties.get_default_directory()}
        self.default_directory = OpenFileField(data, None)
        vbox.add(self.default_directory)

        # Default directory
        data = {"label": _("Default Filename"),
                "value": self.properties.get_default_filename()}
        self.default_filename = StringField(data, None)
        vbox.add(self.default_filename)

        # Error Log File
        data = {"label": _("Error Log File"),
                "value": self.properties.get_error_log_file()}
        self.error_log_file = StringField(data, None)
        vbox.add(self.error_log_file)

        vbox.add(Gtk.Label(_("\nname wildcards:\n" +
                             "\t%d = Date | %n = diagram name |"
                             " %t = time value | %l = language\n")))

        self.show_all()
        response = self.run()

        if response == Gtk.ResponseType.OK:
            self.properties.set_error_log_file(self.error_log_file.get_value())
            self.properties.set_default_directory(
                self.default_directory.get_value())
            self.properties.set_default_filename(
                self.default_filename.get_value())

        self.close()
        self.destroy()
