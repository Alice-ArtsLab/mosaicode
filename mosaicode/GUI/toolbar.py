#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Toolbar class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import gettext
_ = gettext.gettext


class Toolbar(Gtk.Toolbar):
    """
    This class contains methods related the Toolbar class.
    """

    # ----------------------------------------------------------------------
    def __init__(self, main_window):
        """
        This method is the constructor is creates each menu button.
        """
        Gtk.Toolbar.__init__(self)
        self.main_window = main_window
        self.set_style(Gtk.ToolbarStyle.BOTH)
        self.set_hexpand(False)
        self.set_property("expand", False)

        self.actions = {}

        self.__create_button(Gtk.STOCK_NEW,
                             _("New"),
                             self.main_window.main_control.new)
        self.__create_button(Gtk.STOCK_OPEN,
                             _("Open Project"),
                             self.main_window.main_control.select_open)
        self.__create_button(Gtk.STOCK_SAVE,
                             _("Save Project"),
                             self.main_window.main_control.save)

        self.add(Gtk.SeparatorToolItem())
        self.__create_button(Gtk.STOCK_EXECUTE,
                             _("Run"),
                             self.main_window.main_control.run)
        self.__create_button(Gtk.STOCK_INDEX,
                             _("Publish"),
                             self.main_window.main_control.publish)
        self.__create_button(Gtk.STOCK_SELECT_ALL,
                             _("View Source"),
                             self.main_window.main_control.view_source)

        self.add(Gtk.SeparatorToolItem())
        self.__create_button(Gtk.STOCK_ZOOM_OUT,
                             _("Zoom Out"),
                             self.main_window.main_control.zoom_out)
        self.__create_button(Gtk.STOCK_ZOOM_IN,
                             _("Zoom In"),
                             self.main_window.main_control.zoom_in)
        self.__create_button(Gtk.STOCK_ZOOM_100,
                             _("Normal Size"),
                             self.main_window.main_control.zoom_normal)
        self.__create_button(Gtk.STOCK_ZOOM_FIT,
                             _("Fit on screen"),
                             self.main_window.main_control.reload)

        self.add(Gtk.SeparatorToolItem())
        self.__create_button(Gtk.STOCK_GO_UP,
                             _("Align Top"),
                             self.main_window.main_control.align_top)
        self.__create_button(Gtk.STOCK_GO_DOWN,
                             _("Align Bottom"),
                             self.main_window.main_control.align_bottom)
        self.__create_button(Gtk.STOCK_GO_BACK,
                             _("Align Left"),
                             self.main_window.main_control.align_left)
        self.__create_button(Gtk.STOCK_GO_FORWARD,
                             _("Align Right"),
                             self.main_window.main_control.align_right)

        self.show_all()

    # ----------------------------------------------------------------------
    def __create_button(self, stock, name, action):
        """
        This method create a button on menu.

            Parameters:
            Returns:

        """
        button = Gtk.ToolButton.new_from_stock(stock)
        button.set_expand(False)
        button.set_label(name)
        button.set_is_important(True)
        button.connect("clicked", self.__button_clicked, None)
        self.add(button)
        self.actions[button] = action
        return button

    # ----------------------------------------------------------------------
    def __button_clicked(self, widget, data):
        """
        This method monitors if the button was clicked.

            Parameters:

        """
        self.actions[widget]()
