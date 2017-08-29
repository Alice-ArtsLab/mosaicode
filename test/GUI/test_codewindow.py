#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.codewindow import CodeWindow

from mosaicode.GUI.mainwindow import MainWindow

class TestCodeTemplateManager(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        code = "Testando Code Window"
        self.codewindow = CodeWindow(win)
