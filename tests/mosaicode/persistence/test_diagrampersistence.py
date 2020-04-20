from tests.test_base import TestBase
from mosaicode.utils.FileUtils import *
from mosaicode.GUI.comment import Comment
from mosaicode.GUI.block import Block
from mosaicode.control.diagramcontrol import DiagramControl
from mosaicode.persistence.diagrampersistence import DiagramPersistence
from mosaicode.system import System
from mosaicode.model.connectionmodel import ConnectionModel

class PreferencesPersistenceTest(TestBase):

    def test_load_save(self):
        file_name = get_temp_file() + ".mscd"
        diagram_control = self.create_diagram_control()
        diagram = diagram_control.diagram

        diagram.file_name = "."
        DiagramPersistence.save(diagram)

        comment = Comment(diagram)
        diagram.file_name = file_name
        DiagramControl.add_comment(diagram, comment)

        System()
        blocks = System.get_blocks()
        for key in blocks:
            block1 = Block(diagram, blocks[key])
            DiagramControl.add_block(diagram, block1)

        source = None
        source_port = None
        for key in diagram.blocks:
            for port in diagram.blocks[key].ports:
                if not port.is_input():
                    source = diagram.blocks[key]
                    source_port = port
                    break

        sink = None
        sink_port = None
        for key in diagram.blocks:
            for port in diagram.blocks[key].ports:
                if port.is_input():
                    sink = diagram.blocks[key]
                    sink_port = port
                    break

        connection = ConnectionModel(diagram, source, source_port, sink, sink_port)
        DiagramControl.add_connection(diagram, connection)

        block0 = self.create_block(diagram_control)

        DiagramPersistence.save(diagram)

        System.remove_block(blocks.values()[0])
        result = DiagramPersistence.load(diagram)

        os.remove(file_name)
