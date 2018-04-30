import unittest
from abc import ABCMeta
from mosaicode.GUI.block import Block
from mosaicode.GUI.comment import Comment
from mosaicode.GUI.diagram import Diagram
from mosaicode.GUI.mainwindow import MainWindow
from mosaicode.model.blockmodel import BlockModel
from mosaicode.control.diagramcontrol import DiagramControl
from mosaicode.control.blockcontrol import BlockControl
from mosaicode.system import System


class TestBase(unittest.TestCase):
    __metaclass__ = ABCMeta

    def create_main_window(self):
        return MainWindow()

    def create_diagram(self):
        return Diagram(self.create_main_window())

    def create_diagram_control(self):
        diagram_control = DiagramControl(self.create_diagram())
        diagram_control.connectors = []
        diagram_control.language = "language"
        return diagram_control

    def create_block(self, diagram_control=None):
        if diagram_control is None:
            diagram_control = self.create_diagram_control()

        block_model = BlockModel()
        block_model.maxIO = 2

        block = Block(diagram_control.diagram, block_model)
        block.language = "language"
        block.properties = [
            {"name": "test",
             "label": "Test",
             "type": "Test"
             }]

        block.ports = [{"type": "Test",
                       "label": "Input",
                       "conn_type": "Input",
                       "name": "input"},
                        {"type": "Test",
                       "label": "Output",
                       "conn_type": "Outpu",
                       "name": "output"}]

        BlockControl.load_ports(block, System.get_ports())

        DiagramControl.add_block(diagram_control.diagram, block)
        return block

    def create_comment(self):
        comment = Comment(self.create_diagram())
        comment.text = "Test"
        return comment

