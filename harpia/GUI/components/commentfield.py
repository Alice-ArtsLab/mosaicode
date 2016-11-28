import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from harpia.GUI.components.field import Field


class CommentField(Field, Gtk.VBox):

    configuration = {"label": "",
            "value": "",
            "name": "",
            "height": 80,
            "width": 50
            }

    # --------------------------------------------------------------------------
    def __init__(self, data, event):
        if not isinstance(data, dict):
            return
        Field.__init__(self, data, event)
        Gtk.VBox.__init__(self)

        self.check_values()

        self.set_name(self.data["name"])

        self.set_homogeneous(False)
        self.set_spacing(10)
        scrolled_window = Gtk.ScrolledWindow()

        scrolled_window.set_min_content_height(self.data["height"])
        scrolled_window.set_min_content_width(self.data["width"])

        scrolled_window.set_shadow_type(Gtk.ShadowType.ETCHED_IN)

        self.label = Gtk.Label(self.data["label"])
        self.label.set_property("halign", Gtk.Align.START)
        self.add(self.label)

        self.field = Gtk.TextView()
        self.field.set_left_margin(10)
        self.field.set_right_margin(10)
        self.field.set_wrap_mode(Gtk.WrapMode.WORD)
        if event is not None:
            self.field.connect("focus-out-event", event)

        self.text_buffer = self.field.get_buffer()
        self.text_buffer.set_text(self.data["value"])
        scrolled_window.add(self.field)

        self.add(scrolled_window)
        self.show_all()

    # --------------------------------------------------------------------------
    def get_type(self):
        from harpia.GUI.fieldtypes import HARPIA_COMMENT
        return HARPIA_COMMENT

    # --------------------------------------------------------------------------
    def get_value(self):
        return self.text_buffer.get_text(
            self.text_buffer.get_start_iter(),
            self.text_buffer.get_end_iter(),
            True)

    # --------------------------------------------------------------------------
    def set_value(self, value):
        self.text_buffer.set_text(value)

# ------------------------------------------------------------------------------
