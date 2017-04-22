from unittest import TestCase
from harpia.model.blockmodel import BlockModel
from harpia.model.plugin import Plugin

class TestBlockModel(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        plugin = Plugin()
        self.block_model = BlockModel(plugin)

    # ----------------------------------------------------------------------x
    def test_get_output_port_name(self):
        self.block_model.get_output_port_name(10)

    # ----------------------------------------------------------------------x
    def test_get_input_port_name(self):
        self.block_model.get_input_port_name(10)

    # ----------------------------------------------------------------------x
    def test_get_id(self):
        self.block_model.set_id(10)
        id = self.block_model.get_id()
        assert id == 10

    # ----------------------------------------------------------------------x
    def test_set_id(self):
        self.block_model.set_id(10)

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
        self.block_model.set_properties(10)

    # ----------------------------------------------------------------------x
    def test_get_language(self):
        self.block_model.get_language()

    # ----------------------------------------------------------------------x
    def test_get_plugin(self):
        self.block_model.get_plugin()

    # ----------------------------------------------------------------------x
    def test_get_label(self):
        self.block_model.get_description()
        print 1

    # ----------------------------------------------------------------------x
    def test_get_icon(self):
        self.block_model.get_icon()

    # ----------------------------------------------------------------------x
    def test_get_color(self):
        self.block_model.get_color()

    # ----------------------------------------------------------------------x
    def test_get_in_types(self):
        self.block_model.get_in_types()

    # ----------------------------------------------------------------------x
    def test_get_out_types(self):
        self.block_model.get_out_types()

    # ----------------------------------------------------------------------x
    def test_get_group(self):
        self.block_model.get_group()
