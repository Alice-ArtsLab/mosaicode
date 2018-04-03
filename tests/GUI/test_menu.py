#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.menu import Menu

from mosaicode.GUI.mainwindow import MainWindow

class TestMenu(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.menu = Menu(win)

    # ----------------------------------------------------------------------x
    def test_add_example(self):

        # NAO TRATA None
        #example = None
        #self.assertIsNone(self.menu.add_example(example))
        example = "ARQUIVO INEXISTENTE"
        self.assertIsNone(self.menu.add_example(example))


    # ----------------------------------------------------------------------x
    def test_update_recent_file(self):
        self.assertIsNone(self.menu.update_recent_file())

    # ----------------------------------------------------------------------x
    def test_add_recent_file(self):
        recent_file = "Arquivo inválido"
        self.assertIsNone(self.menu.add_recent_file(recent_file))
