#!/usr/bin/env python
 # -*- coding: utf-8 -*-
 
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from harpia.GUI.components.field import Field
from harpia.GUI.fieldtypes import *

class IntField(Field, Gtk.HBox):

    def __init__(self, data, event):
        if not isinstance(data,dict):
            return
        Gtk.HBox.__init__(self, True)
        label = Gtk.Label(data["name"])
        self.add(label)

        self.field = Gtk.SpinButton()
        if "value" in data and "lower" in data and "upper" in data and "step" in data:
            adjustment = Gtk.Adjustment(value = float(data["value"]),
                                    lower = int(data["lower"]),
                                    upper = int(data["upper"]),
                                    step_incr = int(data["step"]),
                                    page_incr=0,#[(upper-lower)/10]?
                                    page_size=0)
            self.field.set_adjustment(adjustment)
        self.field.set_value(float(data["value"]))
        self.field.connect("changed", event)
        self.add(self.field)
        self.show_all()

    def get_type(self):
        return HARPIA_INT

    def get_value(self):
        return self.field.get_value()
