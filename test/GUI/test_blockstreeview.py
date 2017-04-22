from unittest import TestCase
from harpia.GUI.blockstreeview import BlocksTreeView

class TestBlocksTreeView(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.blocks_tree_view = MainControl(win)

    # ----------------------------------------------------------------------x
    def test_search(self):
        self.blocks_tree_view.search()

    # ----------------------------------------------------------------------x
    def test_get_selected_block(self):
        self.blocks_tree_view.get_selected_block()

    