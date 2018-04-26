from tests.test_base import TestBase
from mosaicode.system import System as System
from mosaicode.GUI.blocknotebook import BlockNotebook


class TestBlockNotebook(TestBase):

    def setUp(self):
        self.block_notebook = BlockNotebook(self.create_main_window())
        blocks = System.get_blocks()
        self.block_notebook.update_blocks(blocks)

    def test_update_blocks(self):
        blocks = System.get_blocks()
        self.assertIsNone(self.block_notebook.update_blocks(blocks), "Failed to update blocks")
        self.assertIsNone(self.block_notebook.update_blocks(blocks), "Failed to update blocks")

    def test_search(self):
        query = "Add Float"
        self.assertIsNone(self.block_notebook.search(query))

    def test_get_selected_block(self):
        self.assertIsNone(self.block_notebook.get_selected_block())

