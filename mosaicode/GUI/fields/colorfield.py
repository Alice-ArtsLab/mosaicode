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
        response = self.dialog.run()
        if response == Gtk.ResponseType.OK:
            color_selection = self.dialog.get_color_selection()
            self.color = color_selection.get_current_rgba()
            self.__change_bg_color()
        self.dialog.destroy()

    # --------------------------------------------------------------------------
    def get_value(self):
        if len(self.format) == 6:
            result = '#%02x%02x%02x' % (
                        int(self.color.red * 65535 / 256),
                        int(self.color.green * 65535 / 256),
                        int(self.color.blue * 65535 / 256)
                        )
            return result
        elif len(self.format) == 3:
            result = '#%01x%01x%01x' % (
                    int(self.color.red * 65535 / 4096),
                    int(self.color.green * 65535 / 4096),
                    int(self.color.blue * 65535 / 4096)
                    )
            return result
        result_string = Gdk.RGBA.from_color(self.color).to_string()
        return result_string

    # --------------------------------------------------------------------------
    def __change_bg_color(self):
        self.color_block.modify_bg(
                Gtk.StateType.NORMAL,
                Gdk.Color(
                        self.color.red * 65535,
                        self.color.green * 65535,
                        self.color.blue * 65535)
                )

    # --------------------------------------------------------------------------
    def set_value(self, value):
        color = Gdk.RGBA()
        result = color.parse(value)
        self.color = color
        self.__change_bg_color()
# -----------------------------------------------------------------------------
