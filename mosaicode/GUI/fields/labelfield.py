#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the StringField class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mosaicomponents.field import Field


class LabelField(Field):
    """
    This class contains methods related the StringField class.
    """

    configuration = {"label": "", "value": "", "name": ""}

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

        self.field = Gtk.Label()
        self.field.set_property("halign", Gtk.Align.START)
        self.field.set_property("margin-left", 20)
        value = "None"
        if (self.data["value"] is not None):
            value = self.data["value"]
        self.field.set_text(value)
        self.add(self.field)
        self.show_all()

    # --------------------------------------------------------------------------
    def get_value(self):
        return self.field.get_text()

    # --------------------------------------------------------------------------
    def set_value(self, value):
        self.field.set_text(value)

# --------------------------------------------------------------------------
