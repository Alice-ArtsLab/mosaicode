from tests.mosaicode.test_base import TestBase
from mosaicode.system import System
from mosaicode.control.codetemplatecontrol import CodeTemplateControl
import os

class TestCodeTemplate(TestBase):

    def test_init(self):
        CodeTemplateControl()

    # ----------------------------------------------------------------------
    def test_export_xml(self):
        System()
        System.reload()
        CodeTemplateControl.export_xml()

    # ----------------------------------------------------------------------
    def test_load(self):
        file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "assets",
                                 "codetemplate.xml")
        CodeTemplateControl.load(file_name)

    # ----------------------------------------------------------------------
    def test_add_code_template(self):
        System()
        System.reload()
        code_template = self.create_code_template()
        CodeTemplateControl.add_code_template(code_template)

    # ----------------------------------------------------------------------
    def test_delete_code_template(self):
        pass

    # ----------------------------------------------------------------------
    def test_print_template(self):
        CodeTemplateControl.print_template(self.create_code_template())
