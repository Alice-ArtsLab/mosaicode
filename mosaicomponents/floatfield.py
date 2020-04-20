#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the FloatField class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mosaicomponents.field import Field


class FloatField(Field):
    """
    This class contains methods related the FloatField class.
    """

    configuration = {
        "label": "",
        "value": 0,
        "name": "",
        "lower": -9223372036854775806,
        "upper": 9223372036854775807,
        "step": 0.01,
        "page_increment": 0.1,
        "page_size": 0.1,
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

        self.check_values()
        self.create_label()

        value = 0

        try:
            value = float(self.data["value"])
        except:
            pass

        adjustment = Gtk.Adjustment(value=value,
                            lower=float(self.data["lower"]),
                            upper=float(self.data["upper"]),
                            step_increment=float(self.data["step"]),
                            page_increment=float(self.data["page_increment"]),
                            page_size=float(self.data["page_size"]))

        self.field = Gtk.SpinButton.new(adjustment,
                                    float(self.data["step"]),
                                    float(self.data["digits"]))
        self.field.set_property("margin-left", 20)
        self.field.set_value(value)

        if event is not None:
            self.field.connect("changed", event)
            self.field.connect("value-changed", event)
            self.field.connect("change-value", event)
        self.add(self.field)
        self.show_all()

    # --------------------------------------------------------------------------
    def get_value(self):
        return float(self.field.get_value())

    # --------------------------------------------------------------------------
    def set_value(self, value):
        self.field.set_value(float(value))
# --------------------------------------------------------------------------
