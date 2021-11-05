from tests.mosaicode.test_base import TestBase
from mosaicode.plugins.extensionsmanager.blockpropertyeditor \
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

