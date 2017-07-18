from unittest import TestCase
from mosaicode.GUI.blocknotebook import BlockNotebook

class TestBlockNotebook(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.block_notebook = MainControl(win)

    # ----------------------------------------------------------------------x
    def test_get_current_tab(self):
        self.block_notebook.get_current_tab()

    # ----------------------------------------------------------------------x
    def test_get_tabs(self):
        self.block_notebook.get_tabs()

    