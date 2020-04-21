from tests.mosaicode_tests.test_base import TestBase
from mosaicode.plugins.extensionsmanager.GUI.blockeditor import BlockEditor
from mosaicode.plugins.extensionsmanager.GUI.blockmanager import BlockManager


class TestBlockEditor(TestBase):

    def setUp(self):
        block_manager = BlockManager(self.create_main_window())
        self.widget = BlockEditor(block_manager, self.create_block())

    def test_base(self):
        block_manager = BlockManager(self.create_main_window())
        self.widget = BlockEditor(block_manager, self.create_block())

