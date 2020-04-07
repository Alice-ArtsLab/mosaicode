#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the ColorField class.
"""
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from mosaicomponents.field import Field


class ColorField(Field):
    """
    This class contains methods related the ColorField class.
    """
    configuration = {"label": "",
                     "value": "#ffff00000000",
                     "name": "",
                     "format": "FFFF0000FFFF"}

    # --------------------------------------------------------------------------
    def __init__(self, data, event):
        """
        This method is the constructor.
        """
        if not isinstance(data, dict):
            return
        Field.__init__(self, data, event)

        self.check_values()
        self.create_label()

        box = Gtk.HBox()
        box.set_property("margin-left", 20)
        self.color_block = Gtk.Frame()
        box.add(self.color_block)

        button = Gtk.Button.new_from_icon_name(
            "gtk-select-color", Gtk.IconSize.BUTTON)
        button.connect("clicked", self.on_choose_color)
        box.add(button)
        self.add(box)

        self.parent_window = None
        self.event = event
        self.set_value(self.data["value"])
        self.format = self.data["format"]

        self.show_all()

    # --------------------------------------------------------------------------
    def set_parent_window(self, widget):
        self.parent_window = widget

    # --------------------------------------------------------------------------
    def on_choose_color(self, widget):
        color_selection_dialog = Gtk.ColorSelectionDialog("Select color")
        color_selection_dialog.set_transient_for(self.parent_window)
        if self.event is not None:
            color_selection_dialog.connect("destroy", self.event)
        color_selection = color_selection_dialog.get_color_selection()
        if self.color is not None:
            color_selection.set_current_color(self.color)
        response = color_selection_dialog.run()

        if response == Gtk.ResponseType.OK:
            self.color = color_selection.get_current_color()
            self.color_block.modify_bg(Gtk.StateType.NORMAL, self.color)
        color_selection_dialog.destroy()

    # --------------------------------------------------------------------------
    def get_value(self):
        result_string = self.color.to_string()
        if len(self.format) == 6:
            result = "#" + result_string[1:3] + \
                result_string[5:7] + result_string[9:11]
            return result
        if len(self.format) == 3:
            result = "#" + result_string[1:2] + \
                result_string[5:6] + result_string[9:10]
            return result
        return result_string

    # --------------------------------------------------------------------------
    def set_value(self, value):
        if isinstance(value, int):
            a = value & 255
            b = (value >> 8) & 255
            g = (value >> 16) & 255
            r = (value >> 24) & 255
            value = "rgba(" + str(r) + "," + str(g) + "," + str(b) + \
                    "," + str(a) + ")"

        if ":" in value:
            vlist = value.split(":")
            if len(vlist) == 3:
                value = "rgb(" + vlist[0] + "," + vlist[1] + \
                        "," + vlist[2] + ")"
            if len(vlist) == 4:
                value = "rgba(" + vlist[0] + "," + vlist[1] + \
                        "," + vlist[2] + "," + vlist[3] + ")"

        color = Gdk.RGBA()
        result = color.parse(value)
        self.color = color.to_color()
        self.color_block.modify_bg(Gtk.StateType.NORMAL, self.color)

# -----------------------------------------------------------------------------
