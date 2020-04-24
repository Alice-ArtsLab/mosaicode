from tests.mosaicode_tests.test_base import TestBase
from mosaicode.control.portcontrol import PortControl


class TestPortControl(TestBase):

    def setUp(self):
        self.port_control = PortControl()

    def test_add_port(self):
        PortControl.add_port(self.create_port())

    def test_delete_port(self):
        PortControl.delete_port(self.create_port())

    def test_export_xml(self):
        PortControl.export_xml()

    def test_load(self):
        PortControl.load("test.xml")

    def test_print_port(self):
        PortControl.print_port(self.create_port())

