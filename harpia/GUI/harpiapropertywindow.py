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
        self.set_border_width(10)
        vbox = Gtk.VBox()
        self.add(vbox)


        # Default directory
        hbox = Gtk.HBox()
        vbox.add(hbox)
        hbox.add(Gtk.Label("Default Directory"))
        self.default_directory = Gtk.Entry()
        self.default_directory.set_text(self.properties.get_default_directory())
        hbox.add(self.default_directory)

        browser = Gtk.Button.new_with_label("Browser")
        hbox.pack_start(browser, False, False, 0)
        browser.connect("clicked", self.__on_browser_clicked)

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
        self.ok_button.connect("clicked", self.__on_ok_clicked)
        hbox.add(self.ok_button)

        self.show_all()

    #----------------------------------------------------------------------
    def __on_ok_clicked(self, widget, event=None):
        self.properties.set_error_log_file(self.error_log_file.get_text())
        self.properties.set_default_directory(self.default_directory.get_text())
        self.close()
#----------------------------------------------------------------------
    def __on_browser_clicked(self, widget):
        pass
