#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.propertybox import PropertyBox

from mosaicode.GUI.block import Block
from mosaicode.GUI.diagram import Diagram
from mosaicode.GUI.mainwindow import MainWindow
from mosaicode.model.blockmodel import BlockModel

class TestPropertyBox(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.property_box = PropertyBox(win)

    # ----------------------------------------------------------------------x
    def test_set_block(self):
        diagram = Diagram(MainWindow())
        blockmodel = BlockModel()
        block = Block(diagram, blockmodel)
        self.assertIsNone(self.property_box.set_block(block))

    # ----------------------------------------------------------------------x
    def test_notify(self):

        # NÃO HÁ TRATAMENTO PARA None
        widget = None
        data = None
        self.assertIsNone(self.property_box.notify(widget, data))
