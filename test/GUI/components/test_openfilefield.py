from unittest import TestCase
from harpia.GUI.components.openfilefield import OpenFileField

class TestOpenFileField(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.open_file_field = MainControl(win)

    # ----------------------------------------------------------------------x
    def test_get_type(self):
        self.open_file_field.get_type()

    # ----------------------------------------------------------------------x
    def test_get_value(self):
        self.open_file_field.get_value()

    # ----------------------------------------------------------------------x
    def test_set_parent_window(self):
        self.open_file_field.set_parent_window()

    # ----------------------------------------------------------------------x
    def test_on_choose_file(self):
        self.open_file_field.on_choose_file()
