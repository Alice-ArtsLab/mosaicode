import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from tests.mosaicode_tests.test_base import TestBase
from mosaicode.system import System
from mosaicode.GUI.diagram import Diagram

class TestDiagram(TestBase):

    def setUp(self):
        self.diagram = Diagram(self.create_main_window())

    def test_redraw(self):
        self.diagram.redraw()

    def test_change_zoom(self):
        self.diagram.change_zoom(System.ZOOM_IN)
        self.diagram.change_zoom(System.ZOOM_OUT)
        self.diagram.change_zoom(System.ZOOM_ORIGINAL)

    def test_show_elements(self):
        self.diagram.show_comment_property(self.create_comment())
        self.diagram.show_block_property(self.create_block())

    def test_selection(self):
        block = self.create_block()
        self.diagram.main_window.main_control.add_block(block)
        self.diagram.select_all()
        self.diagram.deselect_all()

    def test_connection(self):
        block = self.create_block()
        self.diagram.start_connection(block, block.ports[0])
        self.diagram.end_connection(block, block.ports[1])

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
