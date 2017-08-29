#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.blockpropertyeditor import BlockPropertyEditor

from mosaicode.GUI.mainwindow import MainWindow
from mosaicode.GUI.diagram import Diagram
from mosaicode.model.blockmodel import BlockModel
from mosaicode.GUI.block import Block
from mosaicode.GUI.blockmanager import BlockManager
from mosaicode.GUI.blockeditor import BlockEditor

class TestBlockPropertyEditor(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow
        diagram = Diagram(win)
        blockmodel = BlockModel()

        block = Block(diagram, blockmodel)

        block_manager = BlockManager(win)
        block_editor = BlockEditor(block_manager, block)

        self.block_property_editor = BlockPropertyEditor(block_editor, block)
