#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the ComboField class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mosaicomponents.field import Field


class ComboField(Field):
    """
    This class contains methods related the ComboField class.
    """

    configuration = {"label": "", "value": "", "name": "", "values": []}

    # ------------------------------------------------------------------------------
    def __init__(self, data, event):
        """
        This method is the constructor.
        """
        if not isinstance(data, dict):
            return
        Field.__init__(self, data, event)

        self.check_values()
        self.create_label()

        self.value = self.data["value"]
        self.field = Gtk.ComboBoxText()
        self.field.set_property("margin-left", 20)
        self.field.set_entry_text_column(0)

        for value in self.data["values"]:
            self.field.append_text(value)
        if self.value in self.data["values"]:
            index = self.data["values"].index(self.value)
            self.field.set_active(index)
        if event is not None:
            self.field.connect("changed", event)
        self.add(self.field)
        self.show_all()

    # ------------------------------------------------------------------------------
    def get_value(self):
        value = self.field.get_active_text()
        if value is not None:
            self.value = value
        return self.value

    # ------------------------------------------------------------------------------
    def set_value(self, value):
        self.value = value
        if self.value in self.data["values"]:
            index = self.data["values"].index(self.value)
            self.field.set_active(index)

# ------------------------------------------------------------------------------
