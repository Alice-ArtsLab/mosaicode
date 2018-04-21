from tests.test_base import TestBase
from mosaicode.GUI.connector import Connector
from mosaicode.GUI.block import Block
from mosaicode.model.port import Port
from gi.repository import GooCanvas
from gi.repository import Gdk

class TestConnector(TestBase):

    def setUp(self):
        port = Port()
        self.source_block = self.create_block()
        self.source_block.ports.append(port)
        self.source_block = Block(self.create_diagram(), self.create_block())
        self.diagram = self.create_diagram()
        self.connector = Connector(
                    self.diagram,
                    self.source_block,
                    port
                    )

    def test_update_flow(self):
        self.connector.input = None
        self.connector.update_flow()
        point = (0,0)
        self.connector.update_flow(point)
        self.connector.input = Block(self.create_diagram(), self.create_block())
        self.connector.input.move(100,100)
        self.connector.input_port = Port()
        self.connector.update_flow()

    def test_events(self):
        gdkevent = Gdk.Event()
        gdkevent.key.type = Gdk.EventType.MOTION_NOTIFY

        self.connector.emit("enter-notify-event", self.connector, gdkevent)
        self.connector.is_selected = True
        self.connector.emit("leave-notify-event", self.connector, gdkevent)

        self.connector.is_selected = False
        gdkevent.key.type = Gdk.EventType.DOUBLE_BUTTON_PRESS
        self.connector.emit("button-press-event", self.connector, gdkevent)
        gdkevent.button = 3
        self.connector.emit("button-press-event", self.connector, gdkevent)
        self.connector.is_selected = True
        self.connector.emit("button-press-event", self.connector, gdkevent)

