from tests.mosaicode_tests.test_base import TestBase
from mosaicode.plugins.extensionsmanager.GUI.blockmanager \
    import BlockManager


class TestBlockManager(TestBase):

    def setUp(self):
        self.widget = BlockManager(
                        None,
                        self.create_block())

    def test_base(self):
        self.widget = BlockManager(
                        None,
                        self.create_block())

