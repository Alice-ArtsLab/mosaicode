from mosaicode.GUI.fieldtypes import *
from tests.mosaicode.test_base import TestBase
from mosaicode.GUI.propertybox import PropertyBox
from mosaicode.GUI.block import Block

class TestPropertyBox(TestBase):

    def setUp(self):
        self.propertybox = PropertyBox(self.create_main_window())

    def test_set_block(self):
        block = Block(self.create_diagram(), self.create_block())
        block.properties = [{"name": "curve",
                            "label": "Curve",
                            "type": MOSAICODE_FLOAT,
                            "value": 800
                            }
                           ]
        self.propertybox.set_block(block)
        block.properties = [{"name": "curve",
                            "label": "Curve",
                            "type": MOSAICODE_OPEN_FILE,
                            "value": "800"
                            }
                           ]
        self.propertybox.set_block(block)
        self.propertybox.notify_block()

    def test_set_comment(self):
        comment = self.create_comment()
        self.propertybox.set_comment(comment)
        comment.properties = []
        self.propertybox.set_comment(comment)
        self.propertybox.notify_comment()

    def test_set_diagram(self):
        diagram = self.create_diagram()
        diagram.code_template = None
        self.propertybox.set_diagram(diagram)
        diagram.code_template = self.create_code_template()
        self.propertybox.set_diagram(diagram)
        self.propertybox.notify_diagram()

