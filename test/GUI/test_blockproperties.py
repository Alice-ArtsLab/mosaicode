from unittest import TestCase
from harpia.GUI.blockproperties import BlockProperties

class TestBlockProperties(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.block_properties = MainControl(win)

    # ----------------------------------------------------------------------x
    def test_set_block(self):
        self.block_properties.set_block()

    