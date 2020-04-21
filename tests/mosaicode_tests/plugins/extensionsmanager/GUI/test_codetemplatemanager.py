from tests.mosaicode_tests.test_base import TestBase
from mosaicode.plugins.extensionsmanager.GUI.codetemplatemanager \
    import CodeTemplateManager


class TestCodeTemplateManager(TestBase):

    def setUp(self):
        self.widget = CodeTemplateManager(self.create_main_window())

    def test_base(self):
        self.widget = CodeTemplateManager(self.create_main_window())

