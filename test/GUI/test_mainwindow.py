#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.mainwindow import MainWindow

class TestMainWindow(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        self.main_window = MainWindow()

    # ----------------------------------------------------------------------x
    def test_update(self):
        self.assertIsNone(self.main_window.update())

    # ----------------------------------------------------------------------x
    def test_set_title(self):
        title = "Testando SET TITLE MAIN WINDOW"
        self.assertIsNone(self.main_window.set_title(title))
