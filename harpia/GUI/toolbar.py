#!/usr/bin/env python
 # -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Toolbar(Gtk.Toolbar):

    def __init__(self, main_window):
        Gtk.Toolbar.__init__(self)
        self.main_window = main_window
        self.set_style(Gtk.ToolbarStyle.BOTH)
        self.set_hexpand(False)
        self.set_property("expand", False)

        self.actions = {}

        self.__create_button(Gtk.STOCK_NEW,
                        "New",
                        self.main_window.main_control.new)
        self.__create_button(Gtk.STOCK_OPEN,
                        "Open Project",
                        self.main_window.main_control.select_open)
        self.__create_button(Gtk.STOCK_SAVE,
                        "Save Project",
                        self.main_window.main_control.save)
        self.__create_button(Gtk.STOCK_EXECUTE,
                        "Run",
                        self.main_window.main_control.run)
        self.__create_button(Gtk.STOCK_EDIT,
                        "Save Source",
                        self.main_window.main_control.save_source)
        self.__create_button(Gtk.STOCK_SELECT_ALL,
                        "View Source",
                        self.main_window.main_control.view_source)
        self.__create_button(Gtk.STOCK_ZOOM_OUT,
                        "Zoom Out",
                        self.main_window.main_control.zoom_out)
        self.__create_button(Gtk.STOCK_ZOOM_IN,
                        "Zoom In",
                        self.main_window.main_control.zoom_in)
        self.__create_button(Gtk.STOCK_ZOOM_100,
                        "Normal Size",
                        self.main_window.main_control.zoom_normal)
        self.__create_button(Gtk.STOCK_ZOOM_FIT,
                        "Fit on screen",
                        self.main_window.main_control.reload)
        self.show_all()


    def __create_button(self, stock, name, action):
        button = Gtk.ToolButton.new_from_stock(stock)
        button.set_expand(False)
        button.set_label(name)
        button.set_is_important(True)
        button.connect("clicked", self.__button_clicked, None)
        self.add(button)
        self.actions[button] = action
        return button

    def __button_clicked(self, widget, data):
        self.actions[widget]()
