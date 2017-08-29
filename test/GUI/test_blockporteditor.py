#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.blockporteditor import BlockPortEditor

from mosaicode.GUI.block import Block
from mosaicode.GUI.diagram import Diagram
from mosaicode.GUI.mainwindow import MainWindow
from mosaicode.GUI.blockmanager import BlockManager
from mosaicode.model.blockmodel import BlockModel

class TestBlockPortEditor(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()

        diagram = Diagram(win)
        blockmodel = BlockModel()
        block = Block(diagram, blockmodel)

        block_manager = BlockManager(win)
        self.blockporteditor = BlockPortEditor (block_manager, block)
