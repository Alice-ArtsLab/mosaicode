from tests.mosaicode_tests.test_base import TestBase
from mosaicode.plugins.extensionsmanager.GUI.blockpropertyeditor \
    import BlockPropertyEditor


class TestBlockPropertyEditor(TestBase):

    def setUp(self):
        self.blockpropertyeditor = BlockPropertyEditor(None, None)
