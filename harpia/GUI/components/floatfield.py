#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from harpia.GUI.fieldtypes import *
from harpia.GUI.components.field import Field


class FloatField(Field, Gtk.HBox):

    # --------------------------------------------------------------------------

    def __init__(self, data, event):
        if not isinstance(data, dict):
            return
        Gtk.HBox.__init__(self, True)

        self.check_value(data, "label", "")
        self.check_value(data, "value", 0)
        self.check_value(data, "lower", 0)
        self.check_value(data, "upper", 9223372036854775807)
        self.check_value(data, "step", 1)
        self.check_value(data, "page_inc", 10)
        self.check_value(data, "page_size", 10)
        self.check_value(data, "digits", 2)

        self.label = Gtk.Label(data["label"])
        self.label.set_property("halign", Gtk.Align.START)
        self.add(self.label)

        adjustment = Gtk.Adjustment(value=float(data["value"]),
                                    lower=int(data["lower"]),
                                    upper=int(data["upper"]),
                                    step_incr=int(data["step"]),
                                    page_incr=int(data["page_inc"]),
                                    page_size=int(data["page_size"]))

        self.field = Gtk.SpinButton()
        self.field.set_adjustment(adjustment)
        self.field.configure(adjustment, 0.0, data["digits"])
        self.field.set_value(float(data["value"]))
        if event is not None:
            self.field.connect("changed", event)
            self.field.connect("value-changed", event)
            self.field.connect("change-value", event)
        self.add(self.field)
        self.show_all()

    # --------------------------------------------------------------------------
    def get_type(self):
        return HARPIA_FLOAT

    # --------------------------------------------------------------------------
    def get_value(self):
        return float(self.field.get_value())

# --------------------------------------------------------------------------
