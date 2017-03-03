"""
This module contains the CodeField class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GtkSource
from harpia.GUI.components.field import Field


class CodeField(Field, Gtk.VBox):
    """
    This class contains methods related the CodeField class.
    """

    configuration = {"label": "",
                     "value": "",
                     "name": "",
                     "height": 80,
                     "width": 50,
                     "language": "c"
                     }

    # --------------------------------------------------------------------------
    def __init__(self, data, event):
        """
        This method is the constructor.
        """
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
        self.pack_start(self.label, False, False, 0)

        lang_manager = GtkSource.LanguageManager()
        self.text_buffer = GtkSource.Buffer.new_with_language(
            lang_manager.get_language(self.data["language"]))
        self.field = GtkSource.View.new_with_buffer(self.text_buffer)
        self.field.set_show_line_numbers(True)
        self.field.set_left_margin(10)
        self.field.set_right_margin(10)
        self.field.get_buffer().set_text(self.data["value"])

        self.field.set_wrap_mode(Gtk.WrapMode.WORD)
        if event is not None:
            self.field.connect("focus-out-event", event)

        scrolled_window.add(self.field)

        self.pack_start(scrolled_window, True, True, 0)
        self.show_all()

    # --------------------------------------------------------------------------
    def get_type(self):
        from harpia.GUI.fieldtypes import HARPIA_CODE
        return HARPIA_CODE

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
