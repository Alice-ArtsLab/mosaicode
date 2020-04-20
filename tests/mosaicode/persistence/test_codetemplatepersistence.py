from tests.test_base import TestBase
from mosaicode.utils.FileUtils import *
from mosaicode.model.codetemplate import CodeTemplate
from mosaicode.model.port import Port
from mosaicode.persistence.codetemplatepersistence import CodeTemplatePersistence
from mosaicode.persistence.portpersistence import PortPersistence

class CodeTemplatePersistenceTest(TestBase):

    def setUp(self):
        self.code_template = CodeTemplate()
        self.code_template.code_parts = ["test"]

    def test_save_python(self):
        result = CodeTemplatePersistence.save_python(self.code_template, "/tmp/")
        self.assertEquals(result, True)

        file_name = "/tmp/" + self.code_template.name.lower().replace(' ', '_') + ".py"
        os.chmod(file_name, 000)
        result = CodeTemplatePersistence.save_python(self.code_template, file_name)
        self.assertEquals(result, False)

        os.remove(file_name)

    def test_load(self):
        # First condition
        result = CodeTemplatePersistence.load_xml("This file does not exist")
        self.assertEquals(result, None)

        # Second condition
        port = Port()
        port.label = "test"
        PortPersistence.save_xml(port, "/tmp/")
        file_name = "/tmp/" + port.type + ".xml"
        result = CodeTemplatePersistence.load_xml(file_name)
        self.assertNotEquals(result, True)
        os.remove(file_name)

        CodeTemplatePersistence.save_xml(self.code_template, "/tmp/")
        file_name = "/tmp/" + self.code_template.type + ".xml"
        result = CodeTemplatePersistence.load_xml(file_name)
        self.assertEquals(result, None)
        os.remove(file_name)

        self.code_template.name = "Test"
        CodeTemplatePersistence.save_xml(self.code_template, "/tmp/")
        file_name = "/tmp/" + self.code_template.type + ".xml"
        result = CodeTemplatePersistence.load_xml(file_name)
        self.assertEquals(result.equals(self.code_template), True)
        os.remove(file_name)

    def test_save_xml(self):

        # Second condition
        file_name = "/tmp/" + self.code_template.type + ".xml"
        result = CodeTemplatePersistence.save_xml(self.code_template, "/tmp/")
        os.chmod(file_name, 000)
        result = CodeTemplatePersistence.save_xml(self.code_template, "/tmp/")
        result = CodeTemplatePersistence.save_xml(self.code_template, file_name)
        self.assertEquals(result, False)

        # Second condition
        port = Port()
        port.label = "test"
        PortPersistence.save_xml(port, "/tmp/")
        file_name = "/tmp/" + port.type + ".xml"
        result = CodeTemplatePersistence.load_xml(file_name)
        self.assertNotEquals(result, True)
        os.remove(file_name)

        CodeTemplatePersistence.save_xml(self.code_template, "/tmp/")
        file_name = "/tmp/" + self.code_template.type + ".xml"
        result = CodeTemplatePersistence.load_xml(file_name)
        self.assertEquals(result, None)
        os.remove(file_name)

        self.code_template.name = "Test"
        CodeTemplatePersistence.save_xml(self.code_template, "/tmp/")
        file_name = "/tmp/" + self.code_template.type + ".xml"
        result = CodeTemplatePersistence.load_xml(file_name)
        self.assertNotEquals(result, None)

