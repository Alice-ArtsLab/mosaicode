from tests.mosaicode_tests.test_base import TestBase
from mosaicode.plugins.extensionsmanager.GUI.extensionsmanagermenu \
    import ExtensionsManagerMenu


class TestExtensionsManagerMenu(TestBase):

    def setUp(self):
        self.widget = ExtensionsManagerMenu(self.create_main_window())

    def test_base(self):
        self.widget = ExtensionsManagerMenu(self.create_main_window())

