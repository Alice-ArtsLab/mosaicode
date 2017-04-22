from unittest import TestCase
from harpia.GUI.menu import Menu

class TestMenu(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.menu = MainControl(win)

    # ----------------------------------------------------------------------x
    def test_add_example(self):
        self.menu.add_example()

    # ----------------------------------------------------------------------x
    def test_update_recent_file(self):
        self.menu.update_recent_file()

    