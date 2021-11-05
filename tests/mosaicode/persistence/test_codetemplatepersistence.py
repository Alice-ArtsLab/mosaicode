import os
from tests.mosaicode.test_base import TestBase
from mosaicode.utils.FileUtils import *
from mosaicode.model.codetemplate import CodeTemplate
from mosaicode.model.port import Port
from mosaicode.persistence.codetemplatepersistence import CodeTemplatePersistence
from mosaicode.persistence.portpersistence import PortPersistence
from mosaicode.persistence.blockpersistence import BlockPersistence
from mosaicode.GUI.fieldtypes import *

class CodeTemplatePersistenceTest(TestBase):

    def setUp(self):
        self.code_template = self.create_code_template()

    def test_load_empty(self):
        result = CodeTemplatePersistence.load_xml("This file does not exist")
        self.assertEquals(result, None)

    def test_load_wrong_file(self):
        port = Port()
        port.hint = "test"
        PortPersistence.save_xml(port, path="/tmp/")
        file_name = "/tmp/" + port.hint + ".xml"
        result = CodeTemplatePersistence.load_xml(file_name)
        self.assertNotEquals(result, True)
        os.remove(file_name)

    def test_load_dir(self):
        result = CodeTemplatePersistence.load_xml("/tmp")
        self.assertEquals(result, None)

    def test_load_save(self):
        self.code_template = self.create_code_template()
        CodeTemplatePersistence.save_xml(self.code_template, "/tmp/")
        file_name = "/tmp/" + self.code_template.name + ".xml"
        result = CodeTemplatePersistence.load_xml(file_name)
        os.remove(file_name)

    def test_load_save_empty(self):
        result = CodeTemplatePersistence.save_xml(self.code_template, path=None)
        self.assertEquals(result, False)

    def test_save_wrong_dir(self):
        result = CodeTemplatePersistence.save_xml(self.code_template, path="/nao")
        self.assertEquals(result, False)

    def test_save_exception(self):
        result = CodeTemplatePersistence.save_xml(self.code_template, path="/nao")
        self.assertEquals(result, False)
        result = CodeTemplatePersistence.save_xml(self.code_template, path="/etc")
        self.assertEquals(result, False)

    def test_load_save_empty(self):
        self.code_template.name = ""
        self.code_template.type = ""
        CodeTemplatePersistence.save_xml(self.code_template, "/tmp/")
        file_name = "/tmp/" + self.code_template.type + ".xml"
        result = CodeTemplatePersistence.load_xml(file_name)
        self.assertEquals(result, None)
        os.remove("/tmp/.xml")

