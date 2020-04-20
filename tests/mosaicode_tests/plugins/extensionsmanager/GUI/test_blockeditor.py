from tests.mosaicode_tests.test_base import TestBase
from mosaicode.plugins.extensionsmanager.GUI.blockeditor \
    import BlockEditor


class TestBlockEditor(TestBase):

    def setUp(self):
        self.widget = BlockEditor(
                        None,
                        self.create_block())

    def test_base(self):
        self.widget = BlockEditor(
                        None,
                        self.create_block())

