from tests.test_base import TestBase
from mosaicode.utils.FileUtils import *
from mosaicode.GUI.block import Block
from mosaicode.persistence.blockpersistence import BlockPersistence

class BlockPersistenceTest(TestBase):

    def test_load_save(self):
        diagram_control = self.create_diagram_control()
        block = self.create_block(diagram_control)

        BlockPersistence.save_python(block, "/tmp/")
        file_name = "/tmp/" + block.label.lower().replace(' ', '_') + ".py"
        os.remove(file_name)

        BlockPersistence.save_xml(block, "/tmp/")
        file_name = "/tmp/" + block.type + ".xml"

        result = BlockPersistence.load_xml(file_name)
        os.remove(file_name)
