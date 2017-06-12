from unittest import TestCase
from mosaicode.GUI.block import Block

class TestBlock(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.block = MainControl(win)

    # ----------------------------------------------------------------------x
    def test_rebuild(self):
        self.block.rebuild()

    # ----------------------------------------------------------------------x
    def test_build(self):
        self.block.build()

    # ----------------------------------------------------------------------x
    def test_get_input_pos(self):
        self.block.get_input_pos()

    # ----------------------------------------------------------------------x
    def test_get_output_pos(self):
        self.block.get_output_pos()

    # ----------------------------------------------------------------------x
    def test_move(self):
        self.block.move()

    # ----------------------------------------------------------------------x
    def test_delete(self):
        self.block.delete()

    # ----------------------------------------------------------------------x
    def test_get_position(self):
        self.block.get_position()

    # ----------------------------------------------------------------------x
    def test_set_properties(self):
        self.block.set_properties()

    # ----------------------------------------------------------------------x
    def test_get_properties(self):
        self.block.get_properties()

    # ----------------------------------------------------------------------x
    def test_update_flow(self):
        self.block.update_flow()

    