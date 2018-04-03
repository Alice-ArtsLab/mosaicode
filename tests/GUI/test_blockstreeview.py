#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.blockstreeview import BlocksTreeView

from mosaicode.GUI.mainwindow import MainWindow

class TestBlocksTreeView(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        language = "python"
        self.blocks_tree_view = BlocksTreeView(win, language)

    # ----------------------------------------------------------------------x
    def test_search(self):
        key = 1
        self.assertIsNone(self.blocks_tree_view.search(key))
        key = -1
        self.assertIsNone(self.blocks_tree_view.search(key))

    # ----------------------------------------------------------------------x
    def test_get_selected_block(self):
        self.assertIsNone(self.blocks_tree_view.get_selected_block())
