from tests.mosaicode_tests.test_base import TestBase
from mosaicode.plugins.extensionsmanager.control.extensionsmanagercontrol \
    import ExtensionsManagerControl


class TestExtensionsManagerControl(TestBase):

    def setUp(self):
        self.widget = ExtensionsManagerControl(
                        None,
                        self.create_block())

    def test_base(self):
        self.widget = ExtensionsManagerControl(
                        None,
                        self.create_block())

