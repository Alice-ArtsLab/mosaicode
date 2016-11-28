from unittest import TestCase
from harpia.model.blockmodel import BlockModel


class TestBlockModel(TestCase):

    def test_setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.main_control = MainControl(win)

    # ----------------------------------------------------------------------x
    def test_get_output_port_name(self):
        self.block_model.get_output_port_name()

    # ----------------------------------------------------------------------x
    def test_get_input_port_name(self):
        self.block_model.get_input_port_name()

    # ----------------------------------------------------------------------x
    def test_get_id(self):
        self.block_model.get_id()

    # ----------------------------------------------------------------------x
    def test_set_id(self):
        self.block_model.set_id()

    # ----------------------------------------------------------------------x
    def test_get_type(self):
        self.block_model.get_type()

    # ----------------------------------------------------------------------x
    def test_get_xml(self):
        self.block_model.get_xml()

    # ----------------------------------------------------------------------x
    def test_get_help(self):
        self.block_model.get_help()

    # ----------------------------------------------------------------------x
    def test_get_properties(self):
        self.block_model.get_properties()

    # ----------------------------------------------------------------------x
    def test_set_properties(self):
        self.block_model.set_properties()

    # ----------------------------------------------------------------------x
    def test_get_language(self):
        self.block_model.get_language()

    # ----------------------------------------------------------------------x
    def test_get_plugin(self):
        self.block_model.get_plugin()

    # ----------------------------------------------------------------------x
    def test_get_description(self):
        self.block_model.get_description()

    # ----------------------------------------------------------------------x
    def test_get_position(self):
        self.block_model.get_position()

    # ----------------------------------------------------------------------x
    def test_generate_header(self):
        self.block_model.generate_header()

    # ----------------------------------------------------------------------x
    def test_generate_vars(self):
        self.block_model.generate_vars()

    # ----------------------------------------------------------------------x
    def test_generate_function_call(self):
        self.block_model.generate_function_call()

    # ----------------------------------------------------------------------x
    def test_generate_dealloc(self):
        self.block_model.generate_dealloc()

    # ----------------------------------------------------------------------x
    def test_generate_out_dealloc(self):
        self.block_model.generate_out_dealloc()
