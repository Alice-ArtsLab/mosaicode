#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa: E402
"""
This module contains the Button Bar class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ButtonBar(Gtk.HBox):
    """
    This class contains methods related the Button Bar class
    """

    # ----------------------------------------------------------------------
    def __init__(self):
        Gtk.HBox.__init__(self)

    # ----------------------------------------------------------------------
    def add_button(self, button_data):
        icon_size = Gtk.IconSize.LARGE_TOOLBAR
        icon = Gtk.Image.new_from_icon_name(button_data["icone"], icon_size)
        button = Gtk.ToolButton.new(icon, button_data["data"])
        button.connect("clicked", button_data["action"], button_data["data"])
        self.pack_start(button, False, False, 0)
        self.show_all()
