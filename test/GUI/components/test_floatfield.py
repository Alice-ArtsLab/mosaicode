from unittest import TestCase
from mosaicode.GUI.components.floatfield import FloatField

class TestFloatField(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.float_field = MainControl(win)

    # ----------------------------------------------------------------------x
    def test_get_type(self):
        self.float_field.get_type()

    # ----------------------------------------------------------------------x
    def test_get_value(self):
        self.float_field.get_value()
