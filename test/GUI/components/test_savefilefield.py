from unittest import TestCase
from mosaicode.GUI.components.savefilefield import SaveFileField

class TestSaveFileField(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.save_file_field = MainControl(win)

    # ----------------------------------------------------------------------x
    def test_get_type(self):
        self.save_file_field.get_type()

    # ----------------------------------------------------------------------x
    def test_get_value(self):
        self.save_file_field.get_value()

    # ----------------------------------------------------------------------x
    def test_set_parent_window(self):
        self.save_file_field.set_parent_window()

    # ----------------------------------------------------------------------x
    def test_on_choose_file(self):
        self.save_file_field.on_choose_file()
