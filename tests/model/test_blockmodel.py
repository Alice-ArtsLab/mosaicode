#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.model.blockmodel import BlockModel

from mosaicode.GUI.block import Block
from mosaicode.GUI.diagram import Diagram
from mosaicode.GUI.mainwindow import MainWindow

class TestBlockModel(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        self.blockmodel = BlockModel(None)

    # ----------------------------------------------------------------------x
    def test_get_color(self):
        self.blockmodel.color = "200:200:25:150"
        self.assertIsNotNone(self.blockmodel.get_color())
        self.blockmodel.color = "#F322123ACBED"
        self.assertIsNotNone(self.blockmodel.get_color())
        self.blockmodel.color = ""
        self.assertEqual(0, self.blockmodel.get_color())

    # ----------------------------------------------------------------------x
    def test_get_color_as_rgba(self):

        self.blockmodel.color = "#F322123ACBED"
        self.assertEqual("#F322123ACBED", self.blockmodel.get_color_as_rgba())

        self.blockmodel.color = "200:200:25:150"
        self.assertEqual("rgba(200,200,25,150)", self.blockmodel.get_color_as_rgba())

        self.blockmodel.color = "#F32123"
        self.assertEqual("#F32123", self.blockmodel.get_color_as_rgba())

        self.blockmodel.color = ""
        self.assertEqual("rgba()", self.blockmodel.get_color_as_rgba())

    # ----------------------------------------------------------------------x
    def test_set_properties(self):
        data = None
        self.assertIsNone(self.blockmodel.set_properties(data))
        data = {"label": ("Type"), "name":"type", "value": "True"}
        self.assertIsNone(self.blockmodel.set_properties(data))

    # ----------------------------------------------------------------------x
    def test_get_properties(self):
        self.assertEqual([], self.blockmodel.get_properties())

        self.blockmodel.properties = ["teste1", "teste2", "teste3"]
        self.assertEqual(["teste1", "teste2", "teste3"], self.blockmodel.get_properties())

class TestBlockModel_comBlock(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        diagram = Diagram(MainWindow())
        block = Block(diagram, None)
        self.blockmodel = BlockModel(block)

    # ----------------------------------------------------------------------x
    def test_get_color(self):
        self.blockmodel.color = "200:200:25:150"
        self.assertIsNotNone(self.blockmodel.get_color())
        self.blockmodel.color = "#F322123ACBED"
        self.assertIsNotNone(self.blockmodel.get_color())
        self.blockmodel.color = ""
        self.assertEqual(0, self.blockmodel.get_color())

    # ----------------------------------------------------------------------x
    def test_get_color_as_rgba(self):

        self.blockmodel.color = "#F322123ACBED"
        self.assertEqual("#F322123ACBED", self.blockmodel.get_color_as_rgba())

        self.blockmodel.color = "200:200:25:150"
        self.assertEqual("rgba(200,200,25,150)", self.blockmodel.get_color_as_rgba())

        self.blockmodel.color = "#F32123"
        self.assertEqual("#F32123", self.blockmodel.get_color_as_rgba())

        self.blockmodel.color = ""
        self.assertEqual("rgba()", self.blockmodel.get_color_as_rgba())

    # ----------------------------------------------------------------------x
    def test_set_properties(self):
        data = None
        self.assertIsNone(self.blockmodel.set_properties(data))
        data = {"name":"mosaicode_c_opencv.extensions.opencv.not", "label": "Not", "value": "True"}
        self.assertIsNone(self.blockmodel.set_properties(data))

    # ----------------------------------------------------------------------x
    def test_get_properties(self):
        self.assertEqual([], self.blockmodel.get_properties())

        self.blockmodel.properties = ["teste1", "teste2", "teste3"]
        self.assertEqual(["teste1", "teste2", "teste3"], self.blockmodel.get_properties())
