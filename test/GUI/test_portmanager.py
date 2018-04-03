#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.portmanager import PortManager

from mosaicode.GUI.mainwindow import MainWindow

class TestPortManager(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.menu = PortManager(win)

    # ----------------------------------------------------------------------x
    def test_add_port(self):

        from mosaicode.model.port import Port

        port = Port()
        self.assertIsNone(self.menu.add_port(port))

        # NÃO TRATA None
        # port = None
        # self.assertIsNone(self.menu.add_port(port))
