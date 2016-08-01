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
        label = Gtk.Label(data["name"])
        self.add(label)

	#coloca os valores em variáveis e passa as que existem pro Adjustment
	#Se os caras não existirem, ERRORFIELD NELES!!!
        adjustment = Gtk.Adjustment(value=data["value"],
                                lower=data["lower"],
                                upper=data["upper"],
                                step_incr=data["step"],
                                page_incr=0,
                                page_size=0)
        self.field = Gtk.SpinButton()
        if "digits" in data:
            self.field.configure(adjustment, 0.0, data["digits"])
        else:
            self.field.configure(adjustment, 0.0, 2)
        self.field.set_value(data["value"])
        self.field.connect("changed", event)
        self.add(self.field)
        self.show_all()

    def get_type(self):
        return HARPIA_FLOAT

    def get_value(self):
        return self.field.get_value()
