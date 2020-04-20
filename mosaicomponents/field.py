#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Field class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Field(Gtk.VBox):
    """
    This class contains methods related the Field class.
    """

    configuration = {}
    # ----------------------------------------------------------------------

    def __init__(self, data, event):
        """
        This method is the constructor.
        """
        Gtk.VBox.__init__(self, homogeneous=False)
        self.set_margin_start(5)
        self.set_margin_end(5)
        self.set_margin_top(3)
        self.data = data

    # ----------------------------------------------------------------------
    @classmethod
    def get_configuration(cls):
        return cls.configuration

    # ----------------------------------------------------------------------
    def get_value(self):
        return 0

    # ----------------------------------------------------------------------
    def set_value(self, value):
        pass

    # ----------------------------------------------------------------------
    def create_label(self):
        self.label = Gtk.Label()
        self.label.set_markup("<small>" + self.data["label"] + "</small>")
        self.label.set_property("halign", Gtk.Align.START)
        self.pack_start(self.label, False, False, 0)

    # ----------------------------------------------------------------------
    def check_values(self):
        for key in self.get_configuration():
            if key in self.data:
                continue
            else:
                self.data[key] = self.get_configuration()[key]
        self.set_name(self.data["name"])
