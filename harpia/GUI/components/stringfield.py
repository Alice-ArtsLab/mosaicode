import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from harpia.GUI.components.field import Field
from harpia.GUI.fieldtypes import *

class StringField(Field, Gtk.HBox):

    def __init__(self, data, event):
        if not isinstance(data,dict):
            return
        Gtk.HBox.__init__(self, True)
        label = Gtk.Label(data["name"])
        self.add(label)
        self.field = Gtk.Entry()
        self.field.set_text(data["value"])
        self.field.connect("changed", event)
        self.add(self.field)
        self.show_all()

    def get_type(self):
        return HARPIA_STRING

    def get_value(self):
        return self.field.get_text()
