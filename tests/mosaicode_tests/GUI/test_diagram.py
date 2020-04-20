import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository import GObject

from tests.mosaicode_tests.test_base import TestBase
from mosaicode.GUI.diagram import Diagram

class TestDiagram(TestBase):

    def setUp(self):
        self.diagram = Diagram(self.create_main_window())

    def test_redraw(self):
        self.diagram.redraw()

    def test_event(self):
        event = Gdk.Event()
        event.key.type = Gdk.EventType.KEY_PRESS
        event.state = Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD2_MASK
        event.keyval = Gdk.KEY_a
        self.diagram.emit("check-resize")
        self.diagram.emit("delete_event", event)
        self.diagram.emit("motion-notify-event", event)
        self.diagram.emit("button_press_event", event)
        self.diagram.emit("button_release_event", event)
        self.diagram.emit("key-press-event", event)
#        self.diagram.emit("drag_data_received", event)
