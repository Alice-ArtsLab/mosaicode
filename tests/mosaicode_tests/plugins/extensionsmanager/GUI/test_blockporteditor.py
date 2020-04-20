from tests.mosaicode_tests.test_base import TestBase
from mosaicode.plugins.extensionsmanager.GUI.blockporteditor \
    import BlockPortEditor


class TestBlockPortEditor(TestBase):

    def setUp(self):
        self.widget = BlockPortEditor(
                        None,
                        self.create_block())

    def test_base(self):
        self.widget = BlockPortEditor(
                        None,
                        self.create_block())

