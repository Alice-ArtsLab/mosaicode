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
        self.main_window = self.create_main_window()
        self.diagram = Diagram(self.main_window)
        self.block1 = self.create_block()
        self.main_window.main_control.add_block(self.block1)
        self.block2 = self.create_block()
        self.main_window.main_control.add_block(self.block2)
        self.comment = self.create_comment()
        self.main_window.main_control.add_comment(self.comment)

    def test_redraw(self):
        self.diagram.redraw()

    def test_resize(self):
        self.diagram.resize(None)

    def test_show_block_menu(self):
        event = Gdk.Event().new(Gdk.EventType.BUTTON_PRESS)
        event.button = 3
        self.diagram.show_block_menu(self.block1, event)

    def test_change_zoom(self):
        self.diagram.change_zoom(System.ZOOM_IN)
        self.diagram.change_zoom(System.ZOOM_OUT)
        self.diagram.change_zoom(System.ZOOM_ORIGINAL)

    def test_show_elements(self):
        self.diagram.show_comment_property(self.comment)
        self.diagram.show_block_property(self.block1)

    def test_selection(self):
        self.diagram.select_all()
        self.diagram.deselect_all()

    def test_connection(self):
        self.diagram.start_connection(self.block1, self.block1.ports[0])
        self.diagram.end_connection(self.block2, self.block2.ports[1])

    def test_button_press_event(self):
        event = Gdk.Event().new(Gdk.EventType.BUTTON_PRESS)
        event.button = 1
        event.state = Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.MOD2_MASK
        self.diagram.emit("button_press_event", event)
        self.refresh_gui()
        event.state = Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD2_MASK
        self.diagram.emit("button_press_event", event)
        self.refresh_gui()

        event.button = 2
        self.diagram.emit("button_press_event", event)
        self.refresh_gui()
        event.button = 3
        self.diagram.emit("button_press_event", event)
        self.refresh_gui()

    def test_button_release_event(self):
        event = Gdk.Event().new(Gdk.EventType.BUTTON_PRESS)
        event.button = 1
        event.state = Gdk.ModifierType.BUTTON1_MASK
        self.diagram.emit("button_press_event", event)
        self.refresh_gui()
        self.diagram.emit("button_release_event", event)
        self.refresh_gui()


    def test_motion_notify_event(self):
        self.test_connection()
        event = Gdk.Event().new(Gdk.EventType.BUTTON_PRESS)
        event.button = 1
        event.state = Gdk.ModifierType.BUTTON1_MASK
        self.diagram.emit("button_press_event", event)
        self.refresh_gui()
        self.diagram.emit("motion_notify_event", event)
        self.refresh_gui()
        self.diagram.emit("button_release_event", event)
        self.refresh_gui()

        self.diagram.emit("motion_notify_event", event)
        self.refresh_gui()

        self.diagram.start_connection(self.block1, self.block1.ports[0])
        self.diagram.emit("motion_notify_event", event)
        self.refresh_gui()

    def test_key_press_event(self):
        event = Gdk.Event()
        event.key.type = Gdk.EventType.KEY_PRESS
        event.keyval = Gdk.KEY_Up
        self.diagram.emit("key-press-event", event)
        self.refresh_gui()
        event.keyval = Gdk.KEY_Down
        self.diagram.emit("key-press-event", event)
        self.refresh_gui()
        event.keyval = Gdk.KEY_Left
        self.diagram.emit("key-press-event", event)
        self.refresh_gui()
        event.keyval = Gdk.KEY_Right
        self.diagram.emit("key-press-event", event)
        self.refresh_gui()

        event.state = Gdk.ModifierType.CONTROL_MASK
        event.keyval = Gdk.KEY_Up
        self.diagram.emit("key-press-event", event)
        self.refresh_gui()
        event.keyval = Gdk.KEY_Down
        self.diagram.emit("key-press-event", event)
        self.refresh_gui()
        event.keyval = Gdk.KEY_Left
        self.diagram.emit("key-press-event", event)
        self.refresh_gui()
        event.keyval = Gdk.KEY_Right
        self.diagram.emit("key-press-event", event)
        self.refresh_gui()

        event.state = 0
        self.diagram.focus = True
        event.keyval = Gdk.KEY_Delete
        self.diagram.emit("key-press-event", event)
        self.refresh_gui()

