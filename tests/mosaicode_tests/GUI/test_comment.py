import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository import GObject

from tests.mosaicode_tests.test_base import TestBase
from mosaicode.GUI.comment import Comment

class TestComment(TestBase):

    def setUp(self):
        self.comment = self.create_comment()

    def test_move(self):
        self.comment.move(10,10)

    def test_set_properties(self):
        self.comment.set_properties(None)

    def test_get_properties(self):
        self.comment.get_properties()

    def test_adjust_position(self):
        self.comment.adjust_position()

    def test_update_flow(self):
        self.comment.is_selected = False
        self.comment.focus = False
        self.comment.update_flow()
        self.comment.is_selected = True
        self.comment.focus = True
        self.comment.update_flow()

    def test_button_press_event(self):
        event = Gdk.Event().new(Gdk.EventType.BUTTON_PRESS)
        event.button = 1
        event.state = Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.MOD2_MASK
        self.comment.is_selected = True
        self.comment.emit("button_press_event", self.comment, event)
        self.refresh_gui()
        self.comment.is_selected = False
        self.comment.emit("button_press_event", self.comment, event)
        self.refresh_gui()
        event.state = Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD2_MASK
        self.comment.is_selected = False
        self.comment.emit("button_press_event", self.comment, event)
        self.refresh_gui()

    def test_motion_notify_event(self):
        event = Gdk.Event().new(Gdk.EventType.BUTTON_PRESS)
        event.button = 1
        event.state = Gdk.ModifierType.BUTTON1_MASK
        self.comment.emit("motion_notify_event", self.comment, event)
        self.refresh_gui()
        event.state = Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.MOD2_MASK
        self.comment.emit("motion_notify_event", self.comment, event)
        self.refresh_gui()

    def test_enter_leave_event(self):
        event = Gdk.Event().new(Gdk.EventType.BUTTON_PRESS)
        event.button = 1
        event.state = Gdk.ModifierType.BUTTON1_MASK
        self.comment.emit("enter_notify_event", self.comment, event)
        self.refresh_gui()
        self.comment.emit("leave_notify_event", self.comment, event)
        self.refresh_gui()

