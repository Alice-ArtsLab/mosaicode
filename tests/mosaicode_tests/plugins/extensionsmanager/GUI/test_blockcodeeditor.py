from tests.mosaicode_tests.test_base import TestBase
from mosaicode.plugins.extensionsmanager.GUI.blockmanager import BlockManager
from mosaicode.plugins.extensionsmanager.GUI.blockeditor import BlockEditor
from mosaicode.plugins.extensionsmanager.GUI.blockcodeeditor \
    import BlockCodeEditor


class TestBlockCodeEditor(TestBase):

    def setUp(self):
        block = self.create_block()
        block_manager = BlockManager(self.create_main_window())
        block_editor = BlockEditor(block_manager, block)
        self.widget = BlockCodeEditor(block_editor, block)

    def test_base(self):
        block = self.create_block()
        block_manager = BlockManager(self.create_main_window())
        block_editor = BlockEditor(block_manager, block)
        self.widget = BlockCodeEditor(block_editor, block)

