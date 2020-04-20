from tests.mosaicode_tests.test_base import TestBase
from mosaicode.plugins.extensionsmanager.GUI.extensionsmanagermenu \
    import ExtensionsManagerMenu


class TestExtensionsManagerMenu(TestBase):

    def setUp(self):
        self.widget = ExtensionsManagerMenu(
                        None,
                        self.create_block())

    def test_base(self):
        self.widget = ExtensionsManagerMenu(
                        None,
                        self.create_block())

