import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
import unittest
import threading
from time import sleep
from mosaicomponents.openfilefield import OpenFileField

class TestOpenFileField(unittest.TestCase):

    def setUp(self):
        OpenFileField(None, None)
        self.field = OpenFileField({"label": "test", "value": "False"}, None)
        self.field = OpenFileField({"label": "test", "value": "True"}, None)
        self.field = OpenFileField({}, self.test_value)
        self.field.set_parent_window(None)

    def event(widget, event):
        pass

    def close_window_on_cancel(self):
        self.field.dialog.response(Gtk.ResponseType.CANCEL)
        self.t1.join()

    def close_window_on_ok(self):
        self.field.dialog.select_filename("LICENSE")
        self.field.dialog.response(Gtk.ResponseType.OK)
        self.t1.join()

    def test_click_ok(self):
        self.field = OpenFileField({"value": ""}, self.event)
        self.field.set_parent_window(Gtk.Window.new(Gtk.WindowType.TOPLEVEL))
        # 0 is the label, 1 is the box
        vbox = self.field.get_children()[1]
        # 0 is the frame, 1 is the button
        button = vbox.get_children()[1]
        self.t1 = threading.Thread(target=button.clicked)
        self.t1.start()
        sleep(0.5)
        self.close_window_on_ok()

    def test_click_cancel(self):
        self.field = OpenFileField({ "value": "."}, self.event)
        self.field.set_parent_window(Gtk.Window.new(Gtk.WindowType.TOPLEVEL))
        # 0 is the label, 1 is the box
        vbox = self.field.get_children()[1]
        # 0 is the frame, 1 is the button
        button = vbox.get_children()[1]
        self.t1 = threading.Thread(target=button.clicked)
        self.t1.start()
        sleep(0.5)
        self.close_window_on_cancel()

    def test_value(self):
        value1 = "False"
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')
        value1 = "True"
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')

