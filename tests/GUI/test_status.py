#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.status import Status

from mosaicode.GUI.mainwindow import MainWindow

class TestStatus(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.status = Status(win)

    # ----------------------------------------------------------------------x
    def test_clear(self):
        self.assertIsNone(self.status.clear())

    # ----------------------------------------------------------------------x
    def test_append_text(self):
        text = "TESTE EM STATUS Append_Text"
        self.assertIsNone(self.status.append_text(text))

    # ----------------------------------------------------------------------x
    def test_log(self):
        text = "TESTE EM STATUS Log"
        self.assertIsNone(self.status.log(text))
