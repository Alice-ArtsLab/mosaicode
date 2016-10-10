from unittest import TestCase
from harpia.control.maincontrol import MainControl
from harpia.GUI.mainwindow import MainWindow

class TestMainControl(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.main_control = MainControl(win)

    # ----------------------------------------------------------------------
    def test_new(self):
        self.main_control.new()

    # ----------------------------------------------------------------------
    def test_select_open(self):
        self.main_control.select_open()

    # ----------------------------------------------------------------------
    def test_open(self, file_name):
        self.main_control.open("app_data/example/Add Border.hrp")
