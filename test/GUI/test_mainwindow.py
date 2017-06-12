from unittest import TestCase
from mosaicode.GUI.mainwindow import MainWindow

class TestMainWindow(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.main_window = MainControl(win)

    # ----------------------------------------------------------------------x
    def test_set_title(self):
        self.main_window.set_title()

    