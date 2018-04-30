import gi
from gi.repository import GObject
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from tests.test_base import TestBase
from mosaicode.GUI.preferencewindow import PreferenceWindow

class TestPreferenceWindow(TestBase):

    def setUp(self):
        self.preference_window = PreferenceWindow(self.create_main_window())

    def close_window(self):
        self.preference_window.response(Gtk.ResponseType.OK)
        self.preference_window.close()

    def test_event(self):
        GObject.timeout_add(100, self.close_window)
        self.preference_window.run()
        event = Gdk.Event()
        event.key.type = Gdk.EventType.BUTTON_PRESS
        self.preference_window.emit("button-press-event", event)
