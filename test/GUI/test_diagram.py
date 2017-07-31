#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mosaicode.GUI.diagram import Diagram

from mosaicode.GUI.mainwindow import MainWindow
from mosaicode.model.blockmodel import BlockModel
from mosaicode.GUI.block import Block

class TestDiagram(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.diagram = Diagram(win)

        blockmodel = BlockModel()
        self.block = Block(self.diagram, blockmodel)

    # ----------------------------------------------------------------------x
    def test_set_scrolled_window(self):
        frame = None
        self.assertIsNone(self.diagram.set_scrolled_window(frame))
        frame = None
        self.assertIsNone(self.diagram.set_scrolled_window(frame))

    # ----------------------------------------------------------------------x
    def test_update_scrolling(self):
        self.assertIsNone(self.diagram.update_scrolling())

    # ----------------------------------------------------------------------x
    def test_insert_block(self):
        self.assertTrue(self.diagram.insert_block(self.block))
        block = None
        self.assertTrue(self.diagram.insert_block(block))

    # ----------------------------------------------------------------------x
    def test_add_block(self):
        #self.assertFalse(self.diagram.add_block(self.block))
        self.assertTrue(self.diagram.add_block(None))
        self.assertTrue(self.diagram.add_block(None))


    # ----------------------------------------------------------------------x
    def test_start_connection(self):
        output = None
        block = self.block
        self.assertIsNone(self.diagram.start_connection(output, block))

    # ----------------------------------------------------------------------x
    def test_end_connection(self):
        block = None
        block_input = None
        self.assertFalse(self.diagram.end_connection(block, block_input))
        #self.assertTrue(self.diagram.end_connection(block, block_input))

    # ----------------------------------------------------------------------x
    def test_set_show_grid(self):
        booleano = None
        self.assertIsNone(self.diagram.set_show_grid(booleano))
        booleano = True
        self.assertIsNone(self.diagram.set_show_grid(booleano))
        booleano = False
        self.assertIsNone(self.diagram.set_show_grid(booleano))

    # ----------------------------------------------------------------------x
    def test_update_flows(self):
        self.assertIsNone(self.diagram.update_flows())

    # ----------------------------------------------------------------------x
    def test_set_file_name(self):
        file_name = "Testando.txt"
        self.assertIsNone(self.diagram.set_file_name(file_name))

        # COLOCAR ARQUIVO DA PASTA TEST
        file_name = "/home/lucas/Faculdade/2017-1/Iniciacao/Mosaicode/mosaicode/test/files_for_test/input/And.mscd"
        self.assertIsNone(self.diagram.set_file_name(file_name))

    # ----------------------------------------------------------------------x
    def test_set_zoom(self):
        zoom = 0
        self.assertIsNone(self.diagram.set_zoom(zoom))
        zoom = -1
        self.assertIsNone(self.diagram.set_zoom(zoom))
        zoom = -23445
        self.assertIsNone(self.diagram.set_zoom(zoom))

    # ----------------------------------------------------------------------x
    def test_change_zoom(self):

        from mosaicode.system import System as System
        value = 0
        self.assertIsNone(self.diagram.change_zoom(value))
        value = System.ZOOM_IN
        self.assertIsNone(self.diagram.change_zoom(value))
        value = System.ZOOM_OUT
        self.assertIsNone(self.diagram.change_zoom(value))
        value = System.ZOOM_ORIGINAL
        self.assertIsNone(self.diagram.change_zoom(value))

    # ----------------------------------------------------------------------x
    def test_show_block_property(self):
        block = self.block
        self.assertIsNone(self.diagram.show_block_property(block))

    # ----------------------------------------------------------------------x
    def test_resize(self):
        data = {"label": "teste"}
        self.assertIsNone(self.diagram.resize(data))

    # ----------------------------------------------------------------------x
    def test_select_all(self):
        self.assertIsNone(self.diagram.select_all())

    # ----------------------------------------------------------------------x
    def test_move_selected_blocks(self):
        x = 0
        y = 0
        self.assertIsNone(self.diagram.move_selected_blocks(x, y))
        x = 50
        y = 100
        self.assertIsNone(self.diagram.move_selected_blocks(x, y))

    # ----------------------------------------------------------------------x
    def test_check_limit(self):
        x = 0
        y = 0
        block_pos_x = 10
        block_pos_y = 10
        self.assertIsNotNone(self.diagram.check_limit(x, y, block_pos_x, block_pos_y))

    # ----------------------------------------------------------------------x
    def test_get_selected_blocks_id(self):
        self.assertIsNotNone(self.diagram.get_selected_blocks_id())
        self.assertEqual([], self.diagram.get_selected_blocks_id())

    # ----------------------------------------------------------------------x
    def test_delete(self):
        self.assertIsNone(self.diagram.delete())

    # ----------------------------------------------------------------------x
    def test_paste(self):
        self.assertIsNone(self.diagram.paste())

    # ----------------------------------------------------------------------x
    def test_copy(self):
        self.assertIsNone(self.diagram.copy())

    # ----------------------------------------------------------------------x
    def test_cut(self):
        self.assertIsNone(self.diagram.cut())

    # ----------------------------------------------------------------------x
    def test_delete_connection(self):
        connection = None
        self.assertIsNone(self.diagram.delete_connection(connection))

    # ----------------------------------------------------------------------x
    def test_delete_block(self):
        block = self.block
        self.assertIsNone(self.diagram.delete_block(block))

    # ----------------------------------------------------------------------x
    def test_set_modified(self):
        state = True
        self.assertIsNone(self.diagram.set_modified(state))
        state = False
        self.assertIsNone(self.diagram.set_modified(state))
        state = None
        self.assertIsNone(self.diagram.set_modified(state))

    # ----------------------------------------------------------------------x
    def test_grab_focus(self):
        self.assertIsNone(self.diagram.grab_focus())

    # ----------------------------------------------------------------------x
    def test_redraw(self):
        self.assertIsNone(self.diagram.redraw())

    # ----------------------------------------------------------------------x
    def test_do(self):
        new_msg = "Testando Mensagens"
        self.assertIsNone(self.diagram.do(new_msg))
        #new_msg = 12
        #self.assertIsNone(self.diagram.do(new_msg))

    # ----------------------------------------------------------------------x
    def test_undo(self):
        self.assertIsNone(self.diagram.undo())

    # ----------------------------------------------------------------------x
    def test_redo(self):
        self.assertIsNone(self.diagram.redo())

    # ----------------------------------------------------------------------x
    def test_get_min_max(self):
        self.assertIsNotNone(self.diagram.get_min_max())

    # ----------------------------------------------------------------------x
    def test_align_top(self):
        self.assertIsNone(self.diagram.align_top())

    # ----------------------------------------------------------------------x
    def test_align_bottom(self):
        self.assertIsNone(self.diagram.align_bottom())

    # ----------------------------------------------------------------------x
    def test_align_left(self):
        self.assertIsNone(self.diagram.align_left())

    # ----------------------------------------------------------------------x
    def test_align_right(self):
        self.assertIsNone(self.diagram.align_right())
