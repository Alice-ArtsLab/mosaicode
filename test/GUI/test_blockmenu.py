#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from mosaicode.GUI.mainwindow import MainWindow
from mosaicode.GUI.diagram import Diagram
from mosaicode.GUI.block import Block
from mosaicode.model.blockmodel import BlockModel
from mosaicode.GUI.blockmenu import BlockMenu

class TestBlockMenu(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        diagram = Diagram(MainWindow())
        blockmodel = BlockModel()
        self.block = Block(diagram, blockmodel)
        self.blockmenu = BlockMenu(self.block, None)

#    def test_blockmenu_edit(self):
#        self.assertIsNone(self.blockmenu(self.block, self.__edit_clicked))
