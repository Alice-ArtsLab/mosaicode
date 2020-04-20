from tests.mosaicode_tests.test_base import TestBase
from mosaicode.plugins.extensionsmanager.GUI.porteditor import PortEditor


class TestPortEditor(TestBase):

    def setUp(self):
        self.widget = PortEditor(
                        None,
                        self.create_block())

    def test_base(self):
        self.widget = PortEditor(
                        None,
                        self.create_block())

