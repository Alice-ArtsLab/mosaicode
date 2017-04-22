"""
This module contains the StringField class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from harpia.GUI.components.field import Field


class StringField(Field, Gtk.HBox):
    """
    This class contains methods related the StringField class.
    """

    configuration = {"label": "", "value": "", "name": "", "maxlength": 0}

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

        self.field = Gtk.Entry()
        self.field.set_text(self.data["value"])
        self.field.set_property("max-length", int(self.data["maxlength"]))
        if event is not None:
            self.field.connect("changed", event)
        self.add(self.field)
        self.show_all()

    # --------------------------------------------------------------------------
    def get_type(self):
        from harpia.GUI.fieldtypes import HARPIA_STRING
        return HARPIA_STRING

    # --------------------------------------------------------------------------
    def get_value(self):
        return self.field.get_text()

    # --------------------------------------------------------------------------
    def set_value(self, value):
        self.field.set_text(value)

# --------------------------------------------------------------------------
