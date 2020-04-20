from tests.mosaicode_tests.test_base import TestBase
from mosaicode.plugins.extensionsmanager.GUI.codetemplateeditor \
    import CodeTemplateEditor


class TestCodeTemplateEditor(TestBase):

    def setUp(self):
        self.widget = CodeTemplateEditor(
                        None,
                        self.create_block())

    def test_base(self):
        self.widget = CodeTemplateEditor(
                        None,
                        self.create_block())

