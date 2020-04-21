from tests.mosaicode_tests.test_base import TestBase
from mosaicode.plugins.extensionsmanager.GUI.blockmanager import BlockManager
from mosaicode.plugins.extensionsmanager.GUI.blockeditor import BlockEditor
from mosaicode.plugins.extensionsmanager.GUI.blockporteditor \
    import BlockPortEditor


class TestBlockPortEditor(TestBase):

    def setUp(self):
        block = self.create_block()
        block_manager = BlockManager(self.create_main_window())
        block_editor = BlockEditor(block_manager, block)
        self.widget = BlockPortEditor(block_editor, block)

    def test_base(self):
        block = self.create_block()
        block_manager = BlockManager(self.create_main_window())
        block_editor = BlockEditor(block_manager, block)
        self.widget = BlockPortEditor(block_editor, block)
