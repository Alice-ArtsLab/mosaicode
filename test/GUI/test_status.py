from unittest import TestCase
from mosaicode.GUI.status import Status

class TestStatus(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.status = MainControl(win)

    # ----------------------------------------------------------------------x
    def test_clear(self):
        self.status.clear()

    # ----------------------------------------------------------------------x
    def test_append_text(self):
        self.status.append_text()

    # ----------------------------------------------------------------------x
    def test_log(self):
        self.status.log()

    