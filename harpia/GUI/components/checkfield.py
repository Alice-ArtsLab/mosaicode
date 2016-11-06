import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from harpia.GUI.components.field import Field


class CheckField(Field, Gtk.HBox):

    # ------------------------------------------------------------------------------

    configuration = {"label": "", "value": False, "name": ""}

    def __init__(self, data, event):
        if not isinstance(data, dict):
            return
        Field.__init__(self, data, event)
        Gtk.HBox.__init__(self, True)

        self.check_values()

        self.set_name(self.data["name"])
        self.label = Gtk.Label(self.data["label"])
        self.label.set_property("halign", Gtk.Align.START)
        self.add(self.label)

        self.field = Gtk.Switch()

        if isinstance(self.data["value"], str) \
                or isinstance(self.data["value"], unicode):
            if self.data["value"] == "True":
                self.field.set_active(True)
            else:
                self.field.set_active(False)
        elif isinstance(self.data["value"], bool):
            self.field.set_active(self.data["value"])

        if event is not None:
            self.field.connect("notify::active", event)
        self.add(self.field)
        self.show_all()

    # ------------------------------------------------------------------------------
    def get_type(self):
        from harpia.GUI.fieldtypes import *
        return HARPIA_CHECK

    # ------------------------------------------------------------------------------
    def get_value(self):
        return self.field.get_active()

    # ------------------------------------------------------------------------------
    def set_value(self, value):
        return self.field.set_active(value)

# ------------------------------------------------------------------------------
