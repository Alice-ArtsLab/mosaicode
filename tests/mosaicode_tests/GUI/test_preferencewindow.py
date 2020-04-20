import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
from tests.mosaicode_tests.test_base import TestBase
from mosaicode.GUI.preferencewindow import PreferenceWindow

class TestPreferenceWindow(TestBase):

    def setUp(self):
        self.preference_window = PreferenceWindow(self.create_main_window())

    def close_window(self):
        self.preference_window.response(Gtk.ResponseType.OK)
        self.preference_window.close()

    def test_event(self):
        GLib.timeout_add(100, self.close_window)
        self.preference_window.run()
        event = Gdk.Event()
        event.key.type = Gdk.EventType.BUTTON_PRESS
        self.preference_window.emit("button-press-event", event)
