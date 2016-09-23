#!/usr/bin/env python
 # -*- coding: utf-8 -*-
 
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from harpia.GUI.components.field import Field
from harpia.GUI.fieldtypes import *

class FloatField(Field, Gtk.HBox):

    def __init__(self, data, event):
        if not isinstance(data,dict):
            return
        Gtk.HBox.__init__(self, True)
        self.label = Gtk.Label(data["name"])
        self.label.set_property("halign", Gtk.Align.START)
        self.add(self.label)

        step = 0.01
        if step in data:
            step = data["step"]

        lower_value = 0
        if "lower" in data:
            lower_value = data["lower"]

        upper_value = 32000
        if "upper" in data:
            upper_value = data["upper"]


        adjustment = Gtk.Adjustment(value=float(data["value"]),
                                lower=lower_value,
                                upper=upper_value,
                                step_incr=step,
                                page_incr=0,
                                page_size=0)
        self.field = Gtk.SpinButton()
        if "digits" in data:
            self.field.configure(adjustment, 0.0, data["digits"])
        else:
            self.field.configure(adjustment, 0.0, 2)
        self.field.set_value(float(data["value"]))
        if event != None:
            self.field.connect("changed", event)
            self.field.connect("value-changed", event)
            self.field.connect("change-value", event)
        self.add(self.field)
        self.show_all()

    def get_type(self):
        return HARPIA_FLOAT

    def get_value(self):
        return self.field.get_value()
