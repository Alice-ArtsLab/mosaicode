#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.searchbar import SearchBar

from mosaicode.GUI.mainwindow import MainWindow

class TestSearchBar(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.search_bar = SearchBar(win)

    # ----------------------------------------------------------------------x
    def test_search_changed(self):
        data = None
        self.assertIsNotNone(self.search_bar.search_changed(data))

        data = "TESTE DE SEARCH BAR"
        self.assertIsNotNone(self.search_bar.search_changed(data))

        data = "Rotate Image"
        self.assertIsNotNone(self.search_bar.search_changed(data))
