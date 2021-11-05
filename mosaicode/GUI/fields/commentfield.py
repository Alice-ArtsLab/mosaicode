#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the CommentField class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mosaicode.GUI.fields.field import Field


class CommentField(Field):
    """
    This class contains methods related the CommentField class.
    """

    configuration = {"label": "",
                     "value": "",
                     "name": "",
                     "height": 80,
                     "width": 50
                     }

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

        self.set_homogeneous(False)
        self.set_spacing(10)
        scrolled_window = Gtk.ScrolledWindow()

        scrolled_window.set_min_content_height(self.data["height"])
        scrolled_window.set_min_content_width(self.data["width"])

        scrolled_window.set_shadow_type(Gtk.ShadowType.ETCHED_IN)

        self.field = Gtk.TextView()
        self.field.set_left_margin(10)
        self.field.set_right_margin(10)
        self.field.set_wrap_mode(Gtk.WrapMode.WORD)
        if event is not None:
            self.field.connect("focus-out-event", event)

        self.text_buffer = self.field.get_buffer()
        self.text_buffer.set_text(self.data["value"])
        scrolled_window.add(self.field)

        self.add(scrolled_window)
        self.show_all()

    # --------------------------------------------------------------------------
    def get_value(self):
        return self.text_buffer.get_text(
            self.text_buffer.get_start_iter(),
            self.text_buffer.get_end_iter(),
            True)

    # --------------------------------------------------------------------------
    def set_value(self, value):
        self.text_buffer.set_text(value)

# ------------------------------------------------------------------------------
