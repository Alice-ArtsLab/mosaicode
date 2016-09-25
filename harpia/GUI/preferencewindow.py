#!/usr/bin/env python
 # -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

from harpia.constants import *
from harpia import s2idirectory
from harpia.GUI.components.stringfield import StringField
from harpia.GUI.components.openfilefield import OpenFileField

class PreferenceWindow(Gtk.Dialog):

    def __init__(self, main_window, properties):
        Gtk.Dialog.__init__(self, "Code Window", main_window,
                0,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.properties = properties
        box = self.get_content_area()
        vbox = Gtk.VBox()
        box.add(vbox)


        # Default directory
        data = {"name":"Default directory",
                "value":self.properties.get_default_directory()}
        self.default_directory =  OpenFileField(data, None)
        vbox.add(self.default_directory)

        # Default directory
        data = {"name":"Default Filename",
                "value":self.properties.get_default_filename()}
        self.default_filename =  StringField(data, None)
        vbox.add(self.default_filename)

        # Error Log File
        data = {"name":"Error Log File",
                "value":self.properties.get_error_log_file()}
        self.error_log_file =  StringField(data, None)
        vbox.add(self.error_log_file)

        vbox.add(Gtk.Label("\nname wildcards:\n" + \
            "\t%d = Date | %n = diagram name | %t = time value | %l = language\n"))

        self.show_all()
        response = self.run()

        if response == Gtk.ResponseType.OK:
            self.properties.set_error_log_file(self.error_log_file.get_value())
            self.properties.set_default_directory(self.default_directory.get_value())
            self.properties.set_default_filename(self.default_filename.get_value())

        self.close()
        self.destroy()

