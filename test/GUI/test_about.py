#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.about import About
from mosaicode.GUI.mainwindow import MainWindow

class TestAbout(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.about = About(win)
