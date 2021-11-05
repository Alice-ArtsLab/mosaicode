from tests.mosaicode.test_base import TestBase
from mosaicode.plugins.extensionsmanager.codetemplatemanager \
    import CodeTemplateManager


class TestCodeTemplateManager(TestBase):

    def setUp(self):
        self.widget = CodeTemplateManager(self.create_main_window())

    def test_base(self):
        self.widget = CodeTemplateManager(self.create_main_window())

