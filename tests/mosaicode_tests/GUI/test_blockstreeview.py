from tests.mosaicode_tests.test_base import TestBase
from mosaicode.system import System as System
from mosaicode.GUI.blockstreeview import BlocksTreeView


class TestBlocksTreeView(TestBase):

    def setUp(self):
        self.blockstreeview = BlocksTreeView(
                    self.create_main_window(),
                    "javascript",
                    System.get_blocks())

    def test_get_selected_block(self):
        self.blockstreeview.get_selected_block()

