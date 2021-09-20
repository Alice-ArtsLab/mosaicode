from tests.mosaicode.test_base import TestBase
from mosaicode.utils.FileUtils import *
from mosaicode.GUI.comment import Comment
from mosaicode.GUI.block import Block
from mosaicode.GUI.diagram import Diagram
from mosaicode.model.port import Port
from mosaicode.persistence.portpersistence import PortPersistence
from mosaicode.control.diagramcontrol import DiagramControl
from mosaicode.persistence.diagrampersistence import DiagramPersistence
from mosaicode.system import System

class PreferencesPersistenceTest(TestBase):

    def test_load_save(self):
        diagram = self.create_full_diagram()
        diagram.file_name = "/tmp/Diagram.msc"
        result = DiagramPersistence.save(diagram)
        assert result
        result = DiagramPersistence.load(diagram)
        assert result
        os.remove(diagram.file_name)

        diagram = self.create_diagram()
        diagram.file_name = "/tmp/Diagram.msc"
        result = DiagramPersistence.save(diagram)
        assert result
        result = DiagramPersistence.load(diagram)
        assert result
        os.remove(diagram.file_name)

    def test_load_wrong_code_template(self):
        diagram = self.create_full_diagram()
        diagram.code_template = "Fail"
        result = DiagramPersistence.save(diagram)
        assert result
        result = DiagramPersistence.load(diagram)
        assert result
        os.remove(diagram.file_name)

    def test_load_wrong_block(self):
        diagram = self.create_full_diagram()
        diagram_control = self.create_diagram_control()
        diagram = diagram_control.diagram
        block1 = self.create_block()
        block1.type = "Worng Block Type"
        diagram_control.add_block(block1)
        result = DiagramPersistence.save(diagram)
        assert result
        result = DiagramPersistence.load(diagram)
        assert result
        os.remove(diagram.file_name)

    def test_save_exception(self):
        diagram = self.create_full_diagram()
        diagram.file_name = "/etc/Diagram.msc"
        result = DiagramPersistence.save(diagram)
        self.assertEquals(result, (False, 'Permission denied'))

    def test_load_wrong_diagram(self):
        port = Port()
        port.hint = "test"
        PortPersistence.save_xml(port, path="/tmp/")
        file_name = "/tmp/" + port.hint + ".xml"
        result = DiagramPersistence.load(file_name)
        self.assertNotEquals(result, True)

        diagram = self.create_full_diagram()
        diagram.file_name = file_name
        result = DiagramPersistence.load(diagram)
        self.assertNotEquals(result, True)
        os.remove(file_name)

