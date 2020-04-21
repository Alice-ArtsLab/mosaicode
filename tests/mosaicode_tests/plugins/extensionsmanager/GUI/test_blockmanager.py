from tests.mosaicode_tests.test_base import TestBase
from mosaicode.plugins.extensionsmanager.GUI.blockmanager \
    import BlockManager


class TestBlockManager(TestBase):

    def setUp(self):
        self.widget = BlockManager(self.create_main_window())

    def test_update(self):
        self.widget.update()

    def test_add_new_block(self):
        self.widget.add_new_block(self.create_block())

    def test_add_block(self):
        self.widget.add_block(self.create_block())

    def test_set_block(self):
        self.widget.set_block(self.create_block())

