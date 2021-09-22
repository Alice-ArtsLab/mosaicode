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
from mosaicode.GUI.fields.field import Field


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
        self.add(box)

        self.color_block = Gtk.Frame()
        box.add(self.color_block)

        button = Gtk.Button.new_from_icon_name(
            "gtk-select-color", Gtk.IconSize.BUTTON)
        button.connect("clicked", self.__on_choose_color)
        box.add(button)

        self.parent_window = None
        self.event = event
        self.set_value(self.data["value"])
        self.format = self.data["format"]

        self.show_all()

    # --------------------------------------------------------------------------
    def set_parent_window(self, widget):
        self.parent_window = widget

    # --------------------------------------------------------------------------
    def __on_choose_color(self, widget):
        self.dialog = Gtk.ColorSelectionDialog()
        self.dialog.set_title("Select color")
        self.dialog.set_modal(True)
        self.dialog.set_transient_for(self.parent_window)
        if self.event is not None:
            self.dialog.connect("destroy", self.event)
        color_selection = self.dialog.get_color_selection()
        if self.color is not None:
            try:
                color_selection.set_current_rgba(self.color)
            except:
                pass
        response = self.dialog.show()
        if response == Gtk.ResponseType.OK:
            color_selection = self.dialog.get_color_selection()
            self.color = color_selection.get_current_rgba()
            self.color_block.get_style_context().add_class(
                    "frame {background-color: " + self.color.to_string() + ";}")
        self.dialog.destroy()

    # --------------------------------------------------------------------------
    def get_value(self):
        result_string = Gdk.RGBA.from_color(self.color).to_string()
        if len(self.format) == 6:
            result = '#%02x%02x%02x' % (
                        self.color.red / 256,
                        self.color.green / 256,
                        self.color.blue / 256)
            return result
        if len(self.format) == 3:
            result = '#%01x%01x%01x' % (
                    self.color.red / 4096,
                    self.color.green / 4096,
                    self.color.blue / 4096)
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
        self.color_block.get_style_context().add_class(
                "frame {background-color: " + value + ";}")
# -----------------------------------------------------------------------------
