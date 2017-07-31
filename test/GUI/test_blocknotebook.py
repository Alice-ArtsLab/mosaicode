#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.mainwindow import MainWindow
from mosaicode.GUI.blocknotebook import BlockNotebook

# Se for usar o py.test:
# Comentar a linha acima, e descomentar a de baixo
#from mosaicomponents.mosaicomponents.stringfield import StringField

class TestBlockNotebook(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.blocknotebook = BlockNotebook(win)

    # ----------------------------------------------------------------------
    def test_update(self):
        self.assertIsNone(self.blocknotebook.update())

    # ----------------------------------------------------------------------
    def test_search(self):
        query = "Testando"
        self.assertIsNone(self.blocknotebook.search(query))
        query = None
        self.assertIsNone(self.blocknotebook.search(query))

    # ----------------------------------------------------------------------
    def test_get_selected_block(self):
        self.assertIsNone(self.blocknotebook.get_selected_block())
