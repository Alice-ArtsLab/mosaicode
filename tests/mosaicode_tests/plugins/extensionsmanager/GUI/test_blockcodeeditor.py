from tests.mosaicode_tests.test_base import TestBase
from mosaicode.plugins.extensionsmanager.GUI.blockcodeeditor \
    import BlockCodeEditor


class TestBlockCodeEditor(TestBase):

    def setUp(self):
        self.widget = BlockCodeEditor(
                        None,
                        self.create_block())

    def test_base(self):
        self.widget = BlockCodeEditor(
                        None,
                        self.create_block())

