from tests.test_base import TestBase
from mosaicode.utils.FileUtils import *
from mosaicode.model.port import Port
from mosaicode.persistence.portpersistence import PortPersistence

class PortPersistenceTest(TestBase):

    def test_load_save(self):
        port = Port()
        port.label = "test"

        PortPersistence.save_python(port, "/tmp/")
        file_name = "/tmp/" + port.label.lower().replace(' ', '_') + ".py"
        os.remove(file_name)

        PortPersistence.save_xml(port, "/tmp/")
        file_name = "/tmp/" + port.type + ".xml"

        result = PortPersistence.load_xml(file_name)
        os.remove(file_name)
