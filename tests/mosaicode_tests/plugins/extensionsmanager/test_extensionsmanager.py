from tests.mosaicode_tests.test_base import TestBase
from mosaicode.plugins.extensionsmanager.extensionsmanager \
    import ExtensionsManager


class TestExtensionsManager(TestBase):

    def test_load(self):
        extensions_manager = ExtensionsManager()
        extensions_manager.load(self.create_main_window())

