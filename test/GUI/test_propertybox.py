from unittest import TestCase
from harpia.GUI.propertybox import PropertyBox

class TestPropertyBox(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.property_box = MainControl(win)

    # ----------------------------------------------------------------------x
    def test_set_block(self):
        self.property_box.set_block()

    # ----------------------------------------------------------------------x
    def test_notify(self):
        self.property_box.notify()

    