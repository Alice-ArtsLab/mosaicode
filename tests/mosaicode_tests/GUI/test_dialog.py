import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib
from tests.mosaicode_tests.test_base import TestBase
from mosaicode.GUI.dialog import Dialog

class TestDialog(TestBase):

    def setUp(self):
        self.dialog = Dialog()

    def close_window(self):
        event = Gdk.Event()
        event.key.type = Gdk.EventType.BUTTON_PRESS
        self.dialog.dialog.emit("button-press-event", event)
        self.dialog.dialog.response(Gtk.ResponseType.OK)
        self.dialog.dialog.response(Gtk.ResponseType.CANCEL)
        self.dialog.dialog.close()
        self.dialog.dialog.destroy()

    def test_open_dialog(self):
        GLib.timeout_add(100, self.close_window)
        self.dialog.open_dialog("Test", self.create_main_window(), None, None);
        self.close_window();
        GLib.timeout_add(100, self.close_window)
        self.dialog.open_dialog("Test", self.create_main_window(), "jpg", None);
        self.close_window();
        GLib.timeout_add(100, self.close_window)
        self.dialog.open_dialog("Test", self.create_main_window(), "jpg", "/");
        self.close_window();

    def test_save_dialog(self):
        GLib.timeout_add(100, self.close_window)
        self.dialog.save_dialog(self.create_main_window(), "Test", None, None);
        self.close_window();
        GLib.timeout_add(100, self.close_window)
        self.dialog.save_dialog(self.create_main_window(), "Test", "Test", None);
        self.close_window();

    def test_confirm_overwrite(self):
        self.dialog.confirm_overwrite(None, self.create_main_window());
        self.dialog.confirm_overwrite("Test", self.create_main_window());
        self.dialog.confirm_overwrite("Blablabla", self.create_main_window());

    def test_message_dialog(self):
        GLib.timeout_add(100, self.close_window)
        self.dialog.message_dialog("Test Message Dialog",
                "Test", self.create_main_window());

    def test_confirm_dialog(self):
        GLib.timeout_add(100, self.close_window)
        self.dialog.confirm_dialog("Test Confirm Dialog",
                self.create_main_window());
