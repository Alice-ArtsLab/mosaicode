from tests.mosaicode_tests.test_base import TestBase
from mosaicode.system import System
from mosaicode.plugins.extensionsmanager.GUI.codetemplateeditor \
    import CodeTemplateEditor
from mosaicode.plugins.extensionsmanager.GUI.codetemplatemanager \
    import CodeTemplateManager


class TestCodeTemplateEditor(TestBase):

    def setUp(self):
        code_template_manager = CodeTemplateManager(self.create_main_window())
        code_template_name = self.create_code_template()
        self.widget = CodeTemplateEditor(
                code_template_manager,
                code_template_name)

    def test_base(self):
        code_template_manager = CodeTemplateManager(self.create_main_window())
        code_template_name = "Test"
        self.widget = CodeTemplateEditor(
                code_template_manager,
                code_template_name)

