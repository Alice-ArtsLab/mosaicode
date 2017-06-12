from unittest import TestCase
from mosaicode.model.plugin import Plugin


class TestPlugin(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.plugin = MainControl(win)


    # ----------------------------------------------------------------------x
    def test_get_help(self):
        self.plugin.get_help()

    # ----------------------------------------------------------------------x
    def test_get_label(self):
        self.plugin.get_label()

    # ----------------------------------------------------------------------x
    def test_get_icon(self):
        self.plugin.get_icon()

    # ----------------------------------------------------------------------x
    def test_get_color(self):
        self.plugin.get_color()

    # ----------------------------------------------------------------------x
    def test_get_in_types(self):
        self.plugin.get_in_types()

    # ----------------------------------------------------------------------x
    def test_get_out_types(self):
        self.plugin.get_out_types()

    # ----------------------------------------------------------------------x
    def test_get_group(self):
        self.plugin.get_group()

    # ----------------------------------------------------------------------x
    def test_get_output_port_name(self):
        self.plugin.get_output_port_name()

    # ----------------------------------------------------------------------x
    def test_get_input_port_name(self):
        self.plugin.get_input_port_name()

    # ----------------------------------------------------------------------x
    def test_get_position(self):
        self.plugin.get_position()

    # ----------------------------------------------------------------------x
    def test_get_type(self):
        self.plugin.get_type()

    # ----------------------------------------------------------------------x
    def test_get_id(self):
        self.plugin.get_id()

    # ----------------------------------------------------------------------x
    def test_set_id(self):
        self.plugin.set_id()

    # ----------------------------------------------------------------------x
    def test_get_xml(self):
        self.plugin.get_xml()

    # ----------------------------------------------------------------------x
    def test_get_properties(self):
        self.plugin.get_properties()

    # ----------------------------------------------------------------------x
    def test_set_properties(self):
        self.plugin.set_properties()

    # ----------------------------------------------------------------------x
    def test_get_language(self):
        self.plugin.get_language()

    # ----------------------------------------------------------------------x
    def test_get_plugin(self):
        self.plugin.get_plugin()

    # ----------------------------------------------------------------------x
    def test_generate_header(self):
        self.plugin.generate_header()

    # ----------------------------------------------------------------------x
    def test_generate_vars(self):
        self.plugin.generate_vars()

    # ----------------------------------------------------------------------x
    def test_generate_function_call(self):
        self.plugin.generate_function_call()

    # ----------------------------------------------------------------------x
    def test_generate_dealloc(self):
        self.plugin.generate_dealloc()

    # ----------------------------------------------------------------------x
    def test_generate_out_dealloc(self):
        self.plugin.generate_out_dealloc()
