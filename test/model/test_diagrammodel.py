from unittest import TestCase
from harpia.model.diagrammodel import DiagramModel


class TestDiagramModel(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainWindow()
        self.main_control = MainControl(win)

    # ----------------------------------------------------------------------
    def add_block(self):
        self.diagram_model.add_block()

    # ----------------------------------------------------------------------
    def delete_block(self):
        self.diagram_model.delete_block()

    # ----------------------------------------------------------------------
    def add_connection(self):
        self.diagram_model.add_connection()

    # ----------------------------------------------------------------------
    def delete_connection(self):
        self.diagram_model.delete_connection()

    # ----------------------------------------------------------------------
    def connect_blocks(self):
        self.diagram_model.connect_blocks()

    # ----------------------------------------------------------------------
    def set_file_name(self):
        self.diagram_model.set_file_name()

    # ----------------------------------------------------------------------
    def get_file_name(self):
        self.diagram_model.get_file_name()

    # ----------------------------------------------------------------------
    def get_patch_name(self):
        self.diagram_model.get_patch_name()

    # ----------------------------------------------------------------------
    def set_modified(self):
        self.diagram_model.set_modified()

    # ----------------------------------------------------------------------
    def get_modified(self):
        self.diagram_model.get_modified()

    # ----------------------------------------------------------------------
    def set_zoom(self):
        self.diagram_model.set_zoom()

    # ----------------------------------------------------------------------
    def get_zoom(self):
        self.diagram_model.get_zoom()
