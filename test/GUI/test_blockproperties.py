from unittest import TestCase
from mosaicode.GUI.blockproperties import BlockProperties

from mosaicode.GUI.block import Block
from mosaicode.GUI.diagram import Diagram
from mosaicode.GUI.mainwindow import MainWindow
from mosaicode.GUI.blockmanager import BlockManager
from mosaicode.model.blockmodel import BlockModel

class TestBlockProperties(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.block_properties = BlockProperties(win)

    # ----------------------------------------------------------------------x
    def test_set_block(self):

        win = MainWindow()
        diagram = Diagram(win)
        blockmodel = BlockModel()
        block = Block(diagram, blockmodel)

        self.block_properties.set_block(block)
