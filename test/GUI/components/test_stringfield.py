from unittest import TestCase
from harpia.GUI.components.stringfield import StringField

class TestStringField(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.string_field = MainControl(win)

    # ----------------------------------------------------------------------x
    def test_get_type(self):
        self.string_field.get_type()

    # ----------------------------------------------------------------------x
    def test_get_value(self):
        self.string_field.get_value()
