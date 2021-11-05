from tests.mosaicode.test_base import TestBase
from mosaicode.plugins.extensionsmanager.portmanager import PortManager


class TestPortManager(TestBase):

    def setUp(self):
        self.widget = PortManager(self.create_main_window())

    def test_base(self):
        self.widget = PortManager(self.create_main_window())

