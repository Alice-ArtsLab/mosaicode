from tests.mosaicode_tests.test_base import TestBase
from mosaicode.utils.FileUtils import *
from mosaicode.model.blockmodel import BlockModel
from mosaicode.model.port import Port
from mosaicode.persistence.blockpersistence import BlockPersistence

class TestBlockPersistence(TestBase):

    def test_load_save(self):
        # Try to load a nonexistent file
        file_name = "nonexistent_file.nofile"
        result = BlockPersistence.load_xml(file_name)
        assert result is None

        # Try to load a different file
        file_name = os.path.abspath(__file__)
        result = BlockPersistence.load_xml(file_name)
        assert result is None

        # Create, save and load a empty block
        block = BlockModel()
        block.label = "Empty block"

        persistence = BlockPersistence.save_xml(block, "/tmp/")
        file_name = "/tmp/" + block.label + ".xml"
        assert persistence

        result = BlockPersistence.load_xml(file_name)
        assert result is None
        os.remove(file_name)

        # Create, save and load a block
        # save(path is None) and block.file = "/tmp/" + block.label + ".xml"
        diagram_control = self.create_diagram_control()
        block = self.create_block(diagram_control)
        block.file = "/tmp/" + block.label + ".xml"

        persistence = BlockPersistence.save_xml(block)

        assert persistence

        result = BlockPersistence.load_xml(block.file)
        os.remove(block.file)

        assert isinstance(result, BlockModel)

        # Create e save
        # save(path is None) and block.file = Nove
        diagram_control = self.create_diagram_control()
        block = self.create_block(diagram_control)
        block.file = None

        persistence = BlockPersistence.save_xml(block)

        assert not persistence

        # Create, save and load a block
        # save(path not None)
        diagram_control = self.create_diagram_control()
        block = self.create_block(diagram_control)

        persistence = BlockPersistence.save_xml(block, "/tmp/")
        file_name = "/tmp/" + block.label + ".xml"
        assert persistence

        result = BlockPersistence.load_xml(file_name)
        os.remove(file_name)

        assert isinstance(result, BlockModel)

        assert result.type == block.type
        assert result.language == block.language
        assert result.extension == block.extension
        assert result.help == block.help
        assert result.color == block.color
        assert result.label == block.label
        assert result.group == block.group
        assert result.file is not None
        #assert result.maxOI == block.maxOI

        # assert codes
        for key, value in result.codes.items():
            assert key in block.codes.keys()
            assert result.codes[key] == block.codes[key]

        # assert properties
        for result_prop in result.properties:
            match_prop = False

            for block_prop in block.properties:
                match_attr = False

                for result_key, result_value in result_prop.items():

                    if result_key in block_prop:
                        if result_value == block_prop[result_key]:
                            match_attr = True
                            continue
                        else:
                            match_attr = False
                            break
                    else:
                        match_attr = False
                        break

                if match_attr:
                    match_prop = True
                    break

            assert match_prop

        # assert ports
        for result_port in result.ports:
            assert isinstance(result_port, dict)
            match = False

            for block_port in block.ports:
                if result_port["type"] == block_port.type and \
                   result_port["name"] == block_port.name and \
                   result_port["label"] == block_port.label and \
                   result_port["conn_type"] == block_port.conn_type:

                   match = True

            assert match
