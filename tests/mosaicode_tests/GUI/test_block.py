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

    def test_event(self):
        gdkevent = Gdk.Event()
        gdkevent.key.type = Gdk.EventType.MOTION_NOTIFY

        self.block.emit("enter-notify-event", self.block, gdkevent)
        self.block.is_selected = True
        self.block.emit("leave-notify-event", self.block, gdkevent)

        self.block.is_selected = False
        gdkevent.key.type = Gdk.EventType.DOUBLE_BUTTON_PRESS
        self.block.emit("button-press-event", self.block, gdkevent)
        gdkevent.button = 3
        self.block.emit("button-press-event", self.block, gdkevent)
        self.block.is_selected = True
        self.block.emit("button-press-event", self.block, gdkevent)
#        self.block.emit("motion-notify-event", gdkevent)
