import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
import unittest
import threading
from time import sleep
from mosaicomponents.colorfield import ColorField

class TestColorField(unittest.TestCase):

    def setUp(self):
        ColorField(None, None)
        self.field = ColorField({"label": "test", "value": "#fff"}, None)
        self.field = ColorField({"label": "test", "value": "#fff000"}, None)
        self.field = ColorField({}, self.event)
        self.field.set_parent_window(Gtk.Window.new(Gtk.WindowType.TOPLEVEL))

    def close_window(self):
        self.field.dialog.props.ok_button.clicked()
        self.field.dialog.response(Gtk.ResponseType.OK)
        self.t1.join()

    def event(widget, event):
        pass

    def test_click(self):
        data = {"value": "#fff","format": "FFFFFF"}
        self.field = ColorField(data, self.event)
        self.field.set_parent_window(Gtk.Window.new(Gtk.WindowType.TOPLEVEL))
        # 0 is the label, 1 is the box
        vbox = self.field.get_children()[1]
        # 0 is the frame, 1 is the button
        button = vbox.get_children()[1]
        self.t1 = threading.Thread(target=button.clicked)
        self.t1.start()
        sleep(0.5)
        self.close_window()

    def test_value(self):
        self.field = ColorField({"value": "#fff","format": "FFF"}, None)
        value2 = self.field.get_value()
        self.assertEqual("#fff", value2, 'incorrect value')

        self.field = ColorField({"value": "#fff","format": "FFFFFF"}, None)
        value1 = "#f0f0f0"
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')

        self.field = ColorField({"value": "#fff","format": "FFFFFF"}, None)
        value1 = 0
        self.field.set_value(int(value1))
        value2 = self.field.get_value()
        self.assertEqual("#000000", value2, 'incorrect value')

        self.field = ColorField({"value": "#fff","format": ""}, None)
        value1 = "00:00:00:00"
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual("rgb(0,0,0)", value2, 'incorrect value')

        self.field = ColorField({"value": "#fff","format": ""}, None)
        value1 = "00:00:00"
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual("rgb(0,0,0)", value2, 'incorrect value')

