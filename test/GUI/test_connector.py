from unittest import TestCase
from harpia.GUI.connector import Connector

class TestConnector(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.connector = MainControl(win)

    # ----------------------------------------------------------------------x
    def test_delete(self):
        self.connector.delete()

    # ----------------------------------------------------------------------x
    def test_set_end(self):
        self.connector.set_end()

    # ----------------------------------------------------------------------x
    def test_update_tracking(self):
        self.connector.update_tracking()

    # ----------------------------------------------------------------------x
    def test_update_flow(self):
        self.connector.update_flow()

    