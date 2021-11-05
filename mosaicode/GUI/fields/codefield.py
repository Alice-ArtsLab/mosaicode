#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the CodeField class.
"""
from mosaicode.GUI.fields.field import Field
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')
from gi.repository import Gtk
from gi.repository import GtkSource


class CodeField(Field):
    """
    This class contains methods related the CodeField class.
    """

    configuration = {"label": "",
                     "value": "",
                     "name": "",
                     "height": 80,
                     "width": 50,
                     "language": "c"
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


        lang_manager = GtkSource.LanguageManager()
        self.text_buffer = GtkSource.Buffer.new_with_language(
            lang_manager.get_language(self.data["language"]))
        self.field = GtkSource.View.new_with_buffer(self.text_buffer)
        self.field.set_show_line_numbers(True)
        self.field.set_left_margin(2)
        self.field.set_right_margin(2)
        self.field.get_buffer().set_text(self.data["value"])

        self.field.set_wrap_mode(Gtk.WrapMode.WORD)
        if event is not None:
            self.field.connect("focus-out-event", event)

        scrolled_window.add(self.field)

        self.pack_start(scrolled_window, True, True, 0)
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

    # --------------------------------------------------------------------------
    def insert_at_cursor(self, value):
        self.text_buffer.insert_at_cursor(value, len(value))

# ------------------------------------------------------------------------------
