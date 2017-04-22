from unittest import TestCase
from harpia.GUI.components.combofield import ComboField

class TestComboField(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.combo_field = MainControl(win)

    # ----------------------------------------------------------------------x
    def test_get_type(self):
        self.combo_field.get_type()

    # ----------------------------------------------------------------------x
    def test_get_value(self):
        self.combo_field.get_value()
