import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from harpia.GUI.fieldtypes import *
from harpia.GUI.components.field import Field


class ColorField(Field, Gtk.HBox):

    # --------------------------------------------------------------------------

    def __init__(self, data, event):
        if not isinstance(data, dict):
            return
        Gtk.HBox.__init__(self, True)

        self.check_value(data, "label", "")
        self.check_value(data, "value", "#ffff00000000")

        self.event = event
        self.color = Gdk.color_parse(data["value"])
        self.label = Gtk.Label(data["label"])
        self.add(self.label)
        self.label.set_property("halign", Gtk.Align.START)

        self.color_block = Gtk.DrawingArea()
        self.color_block.modify_bg(Gtk.StateType.NORMAL, self.color)
        self.add(self.color_block)

        button = Gtk.Button.new_from_icon_name(
            "gtk-select-color", Gtk.IconSize.BUTTON)
        button.connect("clicked", self.on_choose_color)
        self.add(button)
        self.show_all()

    # --------------------------------------------------------------------------
    def on_choose_color(self, widget):
        color_selection_dialog = Gtk.ColorSelectionDialog("Select color")
        if self.event is not None:
            color_selection_dialog.connect("destroy", self.event)
        color_selection = color_selection_dialog.get_color_selection()
        color_selection.set_current_color(self.color)
        response = color_selection_dialog.run()

        if response == Gtk.ResponseType.OK:
            self.color = color_selection.get_current_color()
            self.color_block.modify_bg(Gtk.StateType.NORMAL, self.color)
        color_selection_dialog.destroy()

    # --------------------------------------------------------------------------
    def get_type(self):
        return HARPIA_COLOR

    # --------------------------------------------------------------------------
    def get_value(self):
        return self.color.to_string()

    # --------------------------------------------------------------------------
    def set_value(self, value):
        try:
            self.color = Gdk.color_parse(value)
            self.color_block.modify_bg(Gtk.StateType.NORMAL, self.color)
        except:
            pass

# ------------------------------------------------------------------------------
