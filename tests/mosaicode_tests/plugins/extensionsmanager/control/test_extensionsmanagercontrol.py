from tests.mosaicode_tests.test_base import TestBase
from mosaicode.plugins.extensionsmanager.control.extensionsmanagercontrol \
    import ExtensionsManagerControl


class TestExtensionsManagerControl(TestBase):

    def setUp(self):
        self.widget = ExtensionsManagerControl(self.create_main_window())

    def test_code_template_manager(self):
        self.widget.code_template_manager()

    def test_block_manager(self):
        self.widget.block_manager()

    def test_port_manager(self):
        self.widget.port_manager()

    def test_export_extensions(self):
        ExtensionsManagerControl.export_extensions()

    def test_export_xml(self):
        ExtensionsManagerControl.export_xml()

    def test_export_xml_dialog(self):
        self.widget.export_xml_dialog()
