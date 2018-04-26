from tests.test_base import TestBase
from mosaicode.GUI.toolbar import Toolbar
from gi.repository import Gdk

class TestToolbar(TestBase):

    def setUp(self):
        self.toolbar = Toolbar(self.create_main_window())

    def test_events(self):
        gdkevent = Gdk.Event()
        gdkevent.key.type = Gdk.EventType.BUTTON_PRESS
        button = self.toolbar.get_children()[0]
        button.emit("button-press-event", gdkevent)

