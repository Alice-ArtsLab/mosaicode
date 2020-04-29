import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository import GObject

from tests.mosaicode_tests.test_base import TestBase
from mosaicode.GUI.block import Block

class TestBlock(TestBase):

    def setUp(self):
        self.block = self.create_block()

    def test_adjust_position(self):
        self.block.adjust_position()

    def test_set_properties(self):
        properties = self.block.get_properties()
        self.block.set_properties(properties)

    def test_get_port_pos(self):
        self.block.get_port_pos(self.block.ports[0])

    def test_update_flow(self):
        self.block.is_selected = False
        self.block.focus = False
        self.block.update_flow()
        self.block.is_selected = True
        self.block.focus = True
        self.block.update_flow()
        self.block.is_colapsed = True
        self.block.update_flow()

    def test_button_press_event(self):
        event = Gdk.Event().new(Gdk.EventType.BUTTON_PRESS)
        event.button = 1
        event.state = Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.MOD2_MASK
        self.block.is_selected = True
        self.block.emit("button_press_event", self.block, event)
        self.refresh_gui()
        self.block.is_selected = False
        self.block.emit("button_press_event", self.block, event)
        self.refresh_gui()
        event.state = Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD2_MASK
        self.block.is_selected = False
        self.block.emit("button_press_event", self.block, event)
        self.refresh_gui()
        event.button = 3
        self.block.emit("button_press_event", self.block, event)
        self.refresh_gui()

    def test_motion_notify_event(self):
        event = Gdk.Event().new(Gdk.EventType.BUTTON_PRESS)
        event.button = 1
        event.state = Gdk.ModifierType.BUTTON2_MASK
        self.block.emit("motion_notify_event", self.block, event)
        self.refresh_gui()

        event.state = Gdk.ModifierType.BUTTON1_MASK
        self.block.emit("motion_notify_event", self.block, event)
        self.refresh_gui()

        event.state = Gdk.ModifierType.BUTTON1_MASK
        self.block.diagram.curr_connector = self.block
        self.block.emit("motion_notify_event", self.block, event)
        self.refresh_gui()

    def test_enter_leave_event(self):
        event = Gdk.Event().new(Gdk.EventType.BUTTON_PRESS)
        event.button = 1
        event.state = Gdk.ModifierType.BUTTON1_MASK
        self.block.emit("enter_notify_event", self.block, event)
        self.refresh_gui()
        self.block.emit("leave_notify_event", self.block, event)
        self.refresh_gui()

