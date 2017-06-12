from unittest import TestCase
from mosaicode.GUI.components.checkfield import CheckField

class TestCheckField(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.check_field = MainControl(win)

    # ----------------------------------------------------------------------x
    def test_get_type(self):
        self.check_field.get_type()

    # ----------------------------------------------------------------------x
    def test_get_value(self):
        self.check_field.get_value()

    
