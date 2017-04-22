from unittest import TestCase
from harpia.GUI.components.field import Field

class TestField(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.field = MainControl(win)

    # ----------------------------------------------------------------------x
    def test_get_type(self):
        self.field.get_type()

    # ----------------------------------------------------------------------x
    def test_get_value(self):
        self.field.get_value()

    # ----------------------------------------------------------------------x
    def test_check_value(self):
        self.field.check_value()
