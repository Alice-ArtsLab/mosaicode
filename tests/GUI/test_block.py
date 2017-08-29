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
        self.block = Block(diagram, blockmodel)

    # ----------------------------------------------------------------------x
    def test_rebuild(self):
        self.assertIsNone(self.block.rebuild())

    # ----------------------------------------------------------------------x
    def test_build(self):
        self.assertIsNone(self.block.build())

    # ----------------------------------------------------------------------x
    def test_get_input_pos(self):
        input_id = 2
        self.assertIsNotNone(self.block.get_input_pos(input_id))
        #self.assertEqual((int, int), self.block.get_input_pos(input_id))

    # ----------------------------------------------------------------------x
    def test_get_output_pos(self):
        output_id = 2
        self.assertIsNotNone(self.block.get_output_pos(output_id))
        #self.assertEqual((int, int), self.block.get_output_pos(output_id))

    # ----------------------------------------------------------------------x
    def test_move(self):
        x = 3
        y = 5
        self.assertIsNone(self.block.move(x, y))
        x = 0
        y = 0
        self.assertIsNone(self.block.move(x, y))

        # NÃO SUPORTA X, Y = NONE
        #x = None
        #y = None
        #self.assertIsNone(self.block.move(x, y))

    # ----------------------------------------------------------------------x
    def test_adjust_position(self):
        self.assertIsNone(self.block.adjust_position())

    # ----------------------------------------------------------------------x
    def test_delete(self):
        self.assertIsNone(self.block.delete())

    # ----------------------------------------------------------------------x
    def test_get_position(self):
        self.assertIsNotNone(self.block.get_position())

    # ----------------------------------------------------------------------x
    def test_set_properties(self):
        data = {"label": ("Type"), "name":"type", "value": "255:255:255:255"}
        self.assertIsNone(self.block.set_properties(data))
        data = {"label": "", "name":"", "value": ""}
        self.assertIsNone(self.block.set_properties(data))
        data = {"label": None, "name":"type", "value": "255:255:255:255"}
        self.assertIsNone(self.block.set_properties(data))

    # ----------------------------------------------------------------------x
    def test_get_properties(self):
        self.assertIsNotNone(self.block.get_properties())

    # ----------------------------------------------------------------------x
    def test_update_flow(self):
        self.assertIsNotNone(self.block.update_flow())
