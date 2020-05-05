from tests.mosaicode_tests.test_base import TestBase
from mosaicode.GUI.toolbar import Toolbar
import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

class TestToolbar(TestBase):

    def setUp(self):
        self.toolbar = Toolbar(self.create_main_window())

    def test_events(self):
        gdkevent = Gdk.Event()
        gdkevent.key.type = Gdk.EventType.BUTTON_PRESS
        button = self.toolbar.get_children()[0]
        button.emit("button-press-event", gdkevent)
        self.refresh_gui()

    def test_update_threads(self):
        self.toolbar.update_threads({"test":[self.create_diagram(), None]})
        self.toolbar.update_threads({"test":[self.create_diagram(), None]})

    def test_click_button(self):
        self.toolbar.actions.keys()[0].emit("clicked")
        self.refresh_gui()

