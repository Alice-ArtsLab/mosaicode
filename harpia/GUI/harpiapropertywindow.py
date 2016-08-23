#!/usr/bin/env python
 # -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

from harpia.constants import *
from harpia import s2idirectory

class HarpiaPropertyWindow(Gtk.Window):

    def __init__(self, main_window, properties):
        Gtk.Window.__init__(self, title="Properties")
        self.properties = properties
        self.set_parent(main_window)

        vbox = Gtk.VBox()
        self.add(vbox)


        # Default directory
        hbox = Gtk.HBox()
        vbox.add(hbox)
        hbox.add(Gtk.Label("Default Directory"))
        self.default_directory = Gtk.Entry()
        self.default_directory.set_text(self.properties.get_default_directory())
        hbox.add(self.default_directory)

        # Error Log File
        hbox = Gtk.HBox()
        vbox.add(hbox)
        hbox.add(Gtk.Label("Error Log File"))
        self.error_log_file = Gtk.Entry()
        self.error_log_file.set_text(self.properties.get_error_log_file())
        hbox.add(self.error_log_file)

        # Error Log File
        hbox = Gtk.HBox()
        vbox.add(hbox)
        self.ok_button = Gtk.Button("Ok")
        self.ok_button.connect("key-press-event", self.__on_key_press)
        hbox.add(self.ok_button)

        self.show_all()

    #----------------------------------------------------------------------
    def __on_key_press(self, widget, event=None):
        self.properties.set_error_log_file(self.error_log_file.get_text())
        self.properties.set_default_directory(self.default_directory.get_text())
        self.close()
#----------------------------------------------------------------------
