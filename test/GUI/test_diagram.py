from unittest import TestCase
from harpia.GUI.diagram import Diagram

class TestDiagram(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.diagram = MainControl(win)

    # ----------------------------------------------------------------------x
    def test_set_scrolled_window(self):
        self.diagram.set_scrolled_window()

    # ----------------------------------------------------------------------x
    def test_update_scrolling(self):
        self.diagram.update_scrolling()

    # ----------------------------------------------------------------------x
    def test_add_block(self):
        self.diagram.add_block()

    # ----------------------------------------------------------------------x
    def test_start_connection(self):
        self.diagram.start_connection()

    # ----------------------------------------------------------------------x
    def test_end_connection(self):
        self.diagram.end_connection()

    # ----------------------------------------------------------------------x
    def test_update_flows(self):
        self.diagram.update_flows()

    # ----------------------------------------------------------------------x
    def test_set_file_name(self):
        self.diagram.set_file_name()

    # ----------------------------------------------------------------------x
    def test_set_zoom(self):
        self.diagram.set_zoom()

    # ----------------------------------------------------------------------x
    def test_change_zoom(self):
        self.diagram.change_zoom()

    # ----------------------------------------------------------------------x
    def test_show_block_property(self):
        self.diagram.show_block_property()

    # ----------------------------------------------------------------------x
    def test_resize(self):
        self.diagram.resize()

    # ----------------------------------------------------------------------x
    def test_select_all(self):
        self.diagram.select_all()

    # ----------------------------------------------------------------------x
    def test_move_selected_blocks(self):
        self.diagram.move_selected_blocks()

    # ----------------------------------------------------------------------x
    def test_delete(self):
        self.diagram.delete()

    # ----------------------------------------------------------------------x
    def test_paste(self):
        self.diagram.paste()

    # ----------------------------------------------------------------------x
    def test_copy(self):
        self.diagram.copy()

    # ----------------------------------------------------------------------x
    def test_cut(self):
        self.diagram.cut()

    # ----------------------------------------------------------------------x
    def test_delete_connection(self):
        self.diagram.delete_connection()

    # ----------------------------------------------------------------------x
    def test_delete_block(self):
        self.diagram.delete_block()

    # ----------------------------------------------------------------------x
    def test_set_modified(self):
        self.diagram.set_modified()

    # ----------------------------------------------------------------------x
    def test_grab_focus(self):
        self.diagram.grab_focus()

    # ----------------------------------------------------------------------x
    def test_redraw(self):
        self.diagram.redraw()

    # ----------------------------------------------------------------------x
    def test_reset_undo(self):
        self.diagram.reset_undo()

    # ----------------------------------------------------------------------x
    def test_do(self):
        self.diagram.do()

    # ----------------------------------------------------------------------x
    def test_undo(self):
        self.diagram.undo()

    # ----------------------------------------------------------------------x
    def test_redo(self):
        self.diagram.redo()

    # ----------------------------------------------------------------------x
    def test_get_min_max(self):
        self.diagram.get_min_max()

    