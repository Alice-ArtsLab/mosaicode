from tests.mosaicode_tests.test_base import TestBase
from mosaicode.plugins.extensionsmanager.GUI.codetemplatemanager \
    import CodeTemplateManager


class TestCodeTemplateManager(TestBase):

    def setUp(self):
        self.widget = CodeTemplateManager(
                        None,
                        self.create_block())

    def test_base(self):
        self.widget = CodeTemplateManager(
                        None,
                        self.create_block())

