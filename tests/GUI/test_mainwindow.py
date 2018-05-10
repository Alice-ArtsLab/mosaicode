from tests.test_base import TestBase
from mosaicode.GUI.mainwindow import MainWindow
from gi.repository import Gdk

class TestMainWindow(TestBase):

    def setUp(self):
        self.main_window = MainWindow()

    def test_set_title(self):
        self.main_window.set_title("Test")

    def test_update(self):
        self.main_window.update()

    def test_event(self):
        event = Gdk.Event()
        event.key.type = Gdk.EventType.KEY_PRESS
        event.state = Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD2_MASK
        event.keyval = Gdk.KEY_a
        self.main_window.emit("key-press-event", event)
        self.main_window.emit("check-resize")
        self.main_window.emit("delete_event", event)

