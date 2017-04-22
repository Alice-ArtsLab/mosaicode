from unittest import TestCase
from harpia.GUI.dialog import Dialog

class TestDialog(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.dialog = MainControl(win)

    # ----------------------------------------------------------------------x
    def test_open_dialog(self):
        self.dialog.open_dialog()

    # ----------------------------------------------------------------------x
    def test_confirm_overwrite(self):
        self.dialog.confirm_overwrite()

    # ----------------------------------------------------------------------x
    def test_save_dialog(self):
        self.dialog.save_dialog()

    # ----------------------------------------------------------------------x
    def test_save_png_dialog(self):
        self.dialog.save_png_dialog()

    # ----------------------------------------------------------------------x
    def test_message_dialog(self):
        self.dialog.message_dialog()

    # ----------------------------------------------------------------------x
    def test_confirm_dialog(self):
        self.dialog.confirm_dialog()

    # ----------------------------------------------------------------------x
    def test_rename_dialog(self):
        self.dialog.rename_dialog()

    