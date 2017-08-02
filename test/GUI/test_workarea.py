#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.workarea import WorkArea

from mosaicode.GUI.mainwindow import MainWindow
from mosaicode.GUI.diagram import Diagram

class TestWorkArea(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.work_area = WorkArea(win)

    # ----------------------------------------------------------------------x
    def test_add_diagram(self):
        # NÃO TRABALHA COM None
        # diagram = None
        # self.assertIsNone(self.work_area.add_diagram(diagram))
        diagram = Diagram(MainWindow())
        self.assertIsNone(self.work_area.add_diagram(diagram))

    # ----------------------------------------------------------------------x
    def test_close_tab(self):

        position = 50
        self.assertTrue(self.work_area.close_tab(position))
        position = None
        self.assertFalse(self.work_area.close_tab(position))

    # ----------------------------------------------------------------------x
    def test_get_current_diagram(self):
        self.assertIsNone(self.work_area.get_current_diagram())

        self.work_area.set_current_page(0)
        self.assertIsNone(self.work_area.get_current_diagram())

        self.work_area.set_current_page(10)
        self.assertIsNone(self.work_area.get_current_diagram())

        self.work_area.set_current_page(-12)
        self.assertIsNone(self.work_area.get_current_diagram())


    # ----------------------------------------------------------------------x
    def test_get_diagrams(self):
        self.assertIsNotNone(self.work_area.get_diagrams())

    # ----------------------------------------------------------------------x
    def test_rename_diagram(self):
        diagram = Diagram(MainWindow())
        self.assertIsNone(self.work_area.rename_diagram(diagram))

    # ----------------------------------------------------------------------x
    def test_resize(self):
        data = None
        self.assertIsNone(self.work_area.resize(data))
        data = {"label": ("Type"), "name":"type", "value": "True"}
        self.assertIsNone(self.work_area.resize(data))

    # ----------------------------------------------------------------------x
    def test_close_tabs(self):
        self.assertTrue(self.work_area.close_tabs())
        #self.assertTrue(self.work_area.close_tabs())
