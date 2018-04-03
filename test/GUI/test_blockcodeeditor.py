#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.block import Block
from mosaicode.GUI.diagram import Diagram
from mosaicode.GUI.mainwindow import MainWindow
from mosaicode.model.blockmodel import BlockModel

class TestBlock(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        diagram = Diagram(MainWindow())
        blockmodel = BlockModel()
        block = Block(diagram, blockmodel)
        blockmodel = BlockModel(None)
        self.blockcodeeditor = BlockCodeEditor(BlockEditor(), Block())
