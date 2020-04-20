from tests.mosaicode_tests.test_base import TestBase
from mosaicode.control.blockcontrol import BlockControl
from mosaicode.system import System
from mosaicode.model.blockmodel import BlockModel
import os

class TestBlockControl(TestBase):
    def test_init(self):
        BlockControl()

    # ----------------------------------------------------------------------
    def test_export_xml(self):
        System.reload()
        BlockControl.export_xml()

    # ----------------------------------------------------------------------
    def test_load_ports(self):
        block = self.create_block()
        # if it is not a dictionary
        block.ports.append("x")

        # if "type" not in port:
        block.ports.append({"label": "Output",
                            "conn_type": "Output",
                            "name": "output"})
        # if "conn_type" not in port
        block.ports.append({"type": "Output",
                            "label": "Output",
                            "name": "output"})

        # Port ok
        block.ports.append({"type": "Output",
                            "label": "Output",
                            "conn_type": "Output",
                            "name": "output"})

        BlockControl.load_ports(block, System.get_ports())

    # ----------------------------------------------------------------------
    def test_load(self):
        file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "block.xml")
        BlockControl.load(file_name)

        file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "block_error.xml")

        block = BlockControl.load(file_name)
        assert isinstance(block, BlockModel)

    # ----------------------------------------------------------------------
    def test_add_new_block(self):
        BlockControl.add_new_block(self.create_block())

    # ----------------------------------------------------------------------
    def test_delete_block(self):
        block = self.create_block()
        file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "test_file")

        f = open(file_name, 'w')
        f.close()
        block.file = file_name
        ok = BlockControl.delete_block(block)
        assert ok

        block = self.create_block()
        block.file = None
        ok = BlockControl.delete_block(self.create_block())
        assert not ok
        
    # ----------------------------------------------------------------------
    def test_print_block(self):
        BlockControl.print_block(self.create_block())
