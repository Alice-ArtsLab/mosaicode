from unittest import TestCase
from harpia.model.connectionmodel import ConnectionModel

class TestConnectionModel(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.main_control = MainControl(win)

    # ----------------------------------------------------------------------
    def test_get_diagram(self):
        self.connection_model.get_diagram()

    # ----------------------------------------------------------------------
    def test_type_match(self):
        self.connection_model.type_match()

    # ----------------------------------------------------------------------
    def test_get_source_port_name(self):
        self.connection_model.get_source_port_name()

    # ----------------------------------------------------------------------
    def test_get_sink_port_name(self):
        self.connection_model.get_sink_port_name()

    # ----------------------------------------------------------------------
    def test_set_end(self):
        self.connection_model.set_end()