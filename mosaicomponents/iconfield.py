#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the IconField class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf
from mosaicomponents.field import Field


class IconField(Field):
    """
    This class contains methods related the IconField class.
    """

    configuration = {"label": "", "value": "", "name": ""}

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
        self.values = []

        self.liststore = Gtk.ListStore(Pixbuf, str)
        # List system stock icons
        ids = Gtk.stock_list_ids()
        ids.sort()
        for stock_id in ids:
            try:
                pixbuf = Gtk.IconTheme.get_default().load_icon(stock_id, 16, 0)
                self.liststore.append([pixbuf, stock_id])
                self.values.append(stock_id)
            except:
                pass

        self.field = Gtk.ComboBox.new_with_model(self.liststore)
        self.field.set_property("margin-left", 20)

        renderer = Gtk.CellRendererPixbuf()
        self.field.pack_start(renderer, False)
        self.field.add_attribute(renderer, "pixbuf", 0)

        renderer = Gtk.CellRendererText()
        self.field.pack_start(renderer, True)
        self.field.add_attribute(renderer, "text", 1)

        if event is not None:
            self.field.connect("changed", event)
        self.add(self.field)
        self.show_all()

    # ------------------------------------------------------------------------------
    def get_value(self):
        value = self.field.get_active()
        if value is not None:
            self.value = value
        return self.value

    # ------------------------------------------------------------------------------
    def set_value(self, value):
        self.value = value
        if self.value in self.values:
            index = self.values.index(self.value)
            self.field.set_active(index)
# ------------------------------------------------------------------------------
