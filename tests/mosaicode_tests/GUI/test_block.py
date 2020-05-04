import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository import GObject

from tests.mosaicode_tests.test_base import TestBase
from mosaicode.GUI.block import Block
from mosaicode.GUI.diagram import Diagram

class TestBlock(TestBase):

    def setUp(self):
        self.main_window = self.create_main_window()
        self.diagram = self.create_diagram(self.main_window)
        self.diagram_control = self.create_diagram_control(self.diagram)
        self.block = self.create_block(self.diagram_control)
        self.main_window.main_control.add_block(self.block)
        self.block1 = self.create_block(self.diagram_control)
        self.main_window.main_control.add_block(self.block1)
        self.diagram.start_connection(self.block, self.block.ports[0])
        self.diagram.end_connection(self.block1, self.block1.ports[1])

        self.block2 = self.create_block(self.diagram_control)
        self.main_window.main_control.add_block(self.block2)
        self.block3= self.create_block(self.diagram_control)
        self.main_window.main_control.add_block(self.block3)
        self.diagram.start_connection(self.block2, self.block2.ports[0])
        self.diagram.end_connection(self.block3, self.block3.ports[1])

        self.diagram.start_connection(self.block1, self.block1.ports[0])
        self.diagram.end_connection(self.block3, self.block3.ports[1])


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
        self.block1.update_flow()
        self.block2.update_flow()

        self.block.is_selected = True
        self.block.focus = True
        self.block.update_flow()

        self.block.is_collapsed = True
        self.block.update_flow()

    def test_port_press_event(self):
        event = Gdk.Event().new(Gdk.EventType.BUTTON_PRESS)
        event.button = 1
        event.state = Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.MOD2_MASK
        port = self.block.widgets["port" + str(self.block.ports[0])]
        port.emit("button_press_event", port, event)
        port.emit("button_release_event", port, event)
        port = self.block.widgets["port" + str(self.block.ports[1])]
        port.emit("button_press_event", port, event)
        port.emit("button_release_event", port, event)
        self.refresh_gui()

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

