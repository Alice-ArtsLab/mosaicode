from unittest import TestCase
from harpia.GUI.components.intfield import IntField

class TestIntField(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.int_field = MainControl(win)

    # ----------------------------------------------------------------------x
    def test_get_type(self):
        self.int_field.get_type()

    # ----------------------------------------------------------------------x
    def test_get_value(self):
        self.int_field.get_value()
