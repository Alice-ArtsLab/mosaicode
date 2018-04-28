from tests.test_base import TestBase
from mosaicode.utils.FileUtils import *
from mosaicode.GUI.block import Block
from mosaicode.persistence.blockpersistence import BlockPersistence
from mosaicode.system import System

class BlockPersistenceTest(TestBase):

    def test_load_save(self):
        diagram_control = self.create_diagram_control()
        block = self.create_block(diagram_control)

        BlockPersistence.save_python(block)
        data_dir = System.get_user_dir() + "/extensions/"
        data_dir = data_dir + block.language + "/" + block.framework + "/"
        file_name = data_dir + block.label.lower().replace(' ', '_') + ".py"
        os.remove(file_name)

        BlockPersistence.save(block)
        data_dir = System.get_user_dir() + "/extensions/"
        data_dir = data_dir + block.language + "/" + block.framework + "/"
        file_name = data_dir + block.type + ".xml"

        result = BlockPersistence.load(file_name)
        os.remove(file_name)
