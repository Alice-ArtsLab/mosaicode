import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from harpia.GUI.components.field import Field
from harpia.GUI.fieldtypes import *

class CheckField(Field, Gtk.HBox):

    def __init__(self, data, event):
        if not isinstance(data,dict):
            return
        Gtk.HBox.__init__(self, True)
        self.label = Gtk.Label(data["name"])
        self.label.set_property("halign", Gtk.Align.START)
        self.add(self.label)

        self.field = Gtk.Switch()
        if isinstance(data["value"], str) or isinstance(data["value"], unicode):
            if data["value"] == "True":
                self.field.set_active(True)
            else:
                self.field.set_active(False)
        elif isinstance(data["value"], bool):
            self.field.set_active(data["value"])

        self.field.connect("notify::active", event)
        self.add(self.field)
        self.show_all()

    def get_type(self):
        return HARPIA_CHECK

    def get_value(self):
        return self.field.get_active()

