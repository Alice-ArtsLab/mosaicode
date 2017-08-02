#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.mainwindow import MainWindow
from mosaicode.GUI.blockmanager import BlockManager
from mosaicode.GUI.diagram import Diagram
from mosaicode.GUI.block import Block
from mosaicode.model.blockmodel import BlockModel

class TestBlockManager(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.blockmanager = BlockManager(win)

        diagram = Diagram(MainWindow())
        blockmodel = BlockModel()
        self.block = Block(diagram, blockmodel)

    # ----------------------------------------------------------------------
    def test_set_block(self):
        self.assertIsNone(self.blockmanager.set_block(self.block))

    # ----------------------------------------------------------------------
    def test_add_block(self):
        # QUALQUER UMA DAS FORMAS ABAIXO APRESENTARÁ NONE
        # self.assertIsNone(self.blockmanager.add_block(self.block))
        # self.assertIsNone(self.blockmanager.add_block(None))

        # self.block.label = "Teste"
        # self.assertIsNone(self.blockmanager.add_block(self.block))

        diagram = Diagram(MainWindow())
        blockmodel = BlockModel()
        block = Block(diagram, blockmodel)

        block.label = "Teste Block manager"

        self.assertIsNone(self.blockmanager.add_block(block))

    # ----------------------------------------------------------------------
    def test_add_new_block(self):
        self.assertIsNone(self.blockmanager.add_new_block(self.block))

    # ----------------------------------------------------------------------
    def test_update(self):
        self.assertIsNone(self.blockmanager.update())
