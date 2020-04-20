from tests.mosaicode_tests.test_base import TestBase
from mosaicode.plugins.extensionsmanager.GUI.blockpropertyeditor \
    import BlockPropertyEditor


class TestBlockPropertyEditor(TestBase):

    def setUp(self):
        self.blockpropertyeditor = BlockPropertyEditor(
                        None,
                        self.create_block())

    def test_base(self):
        self.blockpropertyeditor = BlockPropertyEditor(
                        None,
                        self.create_block())

