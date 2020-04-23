#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the OpenFileField class.
"""
import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mosaicomponents.field import Field


class OpenFileField(Field):
    """
    This class contains methods related the OpenFileField class.
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

        self.file = self.data["value"]
        self.parent_window = None

        box = Gtk.HBox()
        self.field = Gtk.Entry()
        self.field.set_property("margin-left", 20)
        self.field.set_text(self.file)
        if event is not None:
            self.field.connect("changed", event)
        box.pack_start(self.field, True, True, 0)

        button = Gtk.Button.new_from_icon_name("gtk-file", Gtk.IconSize.BUTTON)
        button.connect("clicked", self.__on_choose_file)
        box.pack_start(button, False, False, 0)
        self.add(box)
        self.show_all()

    # --------------------------------------------------------------------------
    def set_parent_window(self, widget):
        self.parent_window = widget

    # --------------------------------------------------------------------------
    def __on_choose_file(self, widget):
        self.dialog = Gtk.FileChooserDialog()
        self.dialog.set_title("Open")
        self.dialog.set_transient_for(self.parent_window)
        self.dialog.set_action(Gtk.FileChooserAction.OPEN)
        self.dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.dialog.add_buttons(Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        self.dialog.set_default_response(Gtk.ResponseType.OK)
        self.dialog.set_filename(self.field.get_text())

        current_dir = ""
        if os.path.isdir(self.field.get_text()):
            current_dir = self.field.get_text()
        else:
            current_dir = os.path.dirname(self.field.get_text())
        self.dialog.set_current_folder(current_dir)

        response = self.dialog.run()
        print response
        if response == Gtk.ResponseType.OK:
            self.field.set_text(self.dialog.get_filename())
        self.dialog.destroy()

    # --------------------------------------------------------------------------
    def get_value(self):
        return self.field.get_text()

    # --------------------------------------------------------------------------
    def set_value(self, value):
        self.field.set_text(value)

# --------------------------------------------------------------------------
