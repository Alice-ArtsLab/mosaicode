from tests.mosaicode.test_base import TestBase
from mosaicode.utils.FileUtils import *
from mosaicode.model.port import Port
from mosaicode.persistence.portpersistence import PortPersistence
from mosaicode.persistence.codetemplatepersistence import CodeTemplatePersistence

class PortPersistenceTest(TestBase):

    def test_load_save(self):
        port = Port()
        port.label = "test"
        port.hint = "test"

        result = PortPersistence.load_xml("/this file does not exist")
        self.assertEquals(result, None)

        result = PortPersistence.save_xml(port, "/etc/")
        self.assertEquals(result, False)

        result = PortPersistence.save_xml(port, "/impossible to create")
        self.assertEquals(result, False)

        result = PortPersistence.save_xml(port, "/tmp/")
        self.assertEquals(result, True)

        file_name = "/tmp/" + port.hint + ".xml"
        result = PortPersistence.load_xml(file_name)
        os.remove(file_name)

        port.type = ""
        result = PortPersistence.save_xml(port, "/tmp/")
        file_name = "/tmp/" + port.hint + ".xml"
        result = PortPersistence.load_xml(file_name)
        self.assertEquals(result, None)
        os.remove(file_name)

        code_template = self.create_code_template()
        CodeTemplatePersistence.save_xml(code_template, "/tmp/")
        file_name = "/tmp/" + code_template.name + ".xml"
        result = PortPersistence.load_xml(file_name)
        os.remove(file_name)

