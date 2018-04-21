from tests.test_base import TestBase
from mosaicode.control.blockcontrol import BlockControl
from mosaicode.system import System

class TestBlockControl(TestBase):

    def test_print_block(self):
        BlockControl.print_block(self.create_block())
    
    def test_load_ports(self):
        block = self.create_block()
        block.ports.append("x")
        block.ports.append({"type": "ERRO!",
                       "label": "Output",
                       "conn_type": "Output",
                       "name": "output"})
        block.ports.append({"label": "Output",
                       "conn_type": "Output",
                       "name": "output"})
        BlockControl.load_ports(block, System.get_ports())

