from unittest import TestCase
from mosaicode.model.diagrammodel import DiagramModel


class TestDiagramModel(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.diagram_model = MainControl(win)

    # ----------------------------------------------------------------------
    def test_add_block(self):
        self.diagram_model.add_block()

    # ----------------------------------------------------------------------
    def test_delete_block(self):
        self.diagram_model.delete_block()

    # ----------------------------------------------------------------------
    def test_add_connection(self):
        self.diagram_model.add_connection()

    # ----------------------------------------------------------------------
    def test_delete_connection(self):
        self.diagram_model.delete_connection()

    # ----------------------------------------------------------------------
    def test_connect_blocks(self):
        self.diagram_model.connect_blocks()

    # ----------------------------------------------------------------------
    def test_set_file_name(self):
        self.diagram_model.set_file_name()

    # ----------------------------------------------------------------------
    def test_get_file_name(self):
        self.diagram_model.get_file_name()

    # ----------------------------------------------------------------------
    def test_get_patch_name(self):
        self.diagram_model.get_patch_name()

    # ----------------------------------------------------------------------
    def test_set_modified(self):
        self.diagram_model.set_modified()

    # ----------------------------------------------------------------------
    def test_get_modified(self):
        self.diagram_model.get_modified()

    # ----------------------------------------------------------------------
    def test_set_zoom(self):
        self.diagram_model.set_zoom()

    # ----------------------------------------------------------------------
    def get_zoom(self):
        self.diagram_model.get_zoom()
