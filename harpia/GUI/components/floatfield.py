#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the FloatField class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from harpia.GUI.components.field import Field


class FloatField(Field, Gtk.HBox):
    """
    This class contains methods related the FloatField class.
    """

    configuration = {
        "label": "",
        "value": 0,
        "name": "",
        "lower": 0,
        "upper": 9223372036854775807,
        "step": 1,
        "page_inc": 10,
        "page_size": 10,
        "digits": 2
    }

    # --------------------------------------------------------------------------
    def __init__(self, data, event):
        """
        This method is the constructor.
        """
        if not isinstance(data, dict):
            return
        Field.__init__(self, data, event)
        Gtk.HBox.__init__(self, True)

        self.check_values()

        self.set_name(self.data["name"])

        self.label = Gtk.Label(self.data["label"])
        self.label.set_property("halign", Gtk.Align.START)
        self.add(self.label)

        adjustment = Gtk.Adjustment(value=float(self.data["value"]),
                                    lower=int(self.data["lower"]),
                                    upper=int(self.data["upper"]),
                                    step_incr=int(self.data["step"]),
                                    page_incr=int(self.data["page_inc"]),
                                    page_size=int(self.data["page_size"]))

        self.field = Gtk.SpinButton()
        self.field.set_adjustment(adjustment)
        self.field.configure(adjustment, 0.0, self.data["digits"])
        self.field.set_value(float(self.data["value"]))
        if event is not None:
            self.field.connect("changed", event)
            self.field.connect("value-changed", event)
            self.field.connect("change-value", event)
        self.add(self.field)
        self.show_all()

    # --------------------------------------------------------------------------
    def get_type(self):
        from harpia.GUI.fieldtypes import HARPIA_FLOAT
        return HARPIA_FLOAT

    # --------------------------------------------------------------------------
    def get_value(self):
        return float(self.field.get_value())

    # --------------------------------------------------------------------------
    def set_value(self, value):
        self.field.set_value(float(value))
# --------------------------------------------------------------------------
