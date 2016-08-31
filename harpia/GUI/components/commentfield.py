import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from harpia.GUI.components.field import Field
from harpia.GUI.fieldtypes import *

class CommentField(Field, Gtk.VBox):

    def __init__(self, data, event):
        if not isinstance(data,dict):
            return
        Gtk.VBox.__init__(self)
        self.set_homogeneous(False)
        self.set_spacing(10)
        scrolled_window = Gtk.ScrolledWindow()

        if "height" in data:
            scrolled_window.set_min_content_height(data["height"])

        if "width" in data:
            scrolled_window.set_min_content_width(data["width"])

        self.label = Gtk.Label(data["name"])
        self.label.set_property("halign", Gtk.Align.START)
        self.add(self.label)

        self.field = Gtk.TextView()
        self.field.set_left_margin(10)
        self.field.set_right_margin(10)
        self.field.set_wrap_mode(Gtk.WrapMode.WORD)
        if event != None:
            self.field.connect("focus-out-event", event)

        self.text_buffer = self.field.get_buffer()
        self.text_buffer.set_text(data["value"])
        scrolled_window.add(self.field)

        self.add(scrolled_window)
        self.show_all()

    def get_type(self):
        return HARPIA_COMMENT
        
    def get_value(self):
        return self.text_buffer.get_text(
                        self.text_buffer.get_start_iter(),
                        self.text_buffer.get_end_iter(),
                        True)
