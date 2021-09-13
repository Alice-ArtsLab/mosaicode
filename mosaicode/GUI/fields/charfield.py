#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the CharField class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mosaicomponents.field import Field


class CharField(Field):
    """
    This class contains methods related the CharField class.
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

        self.field = Gtk.Entry()
        self.field.set_property("margin-left", 20)
        self.field.set_text(self.data["value"])
        self.field.set_property("max-length", 1)
        if event is not None:
            self.field.connect("changed", event)
        self.add(self.field)
        self.show_all()

    # --------------------------------------------------------------------------
    def get_value(self):
        return self.field.get_text()

    # --------------------------------------------------------------------------
    def set_value(self, value):
        self.field.set_text(value)

# --------------------------------------------------------------------------
