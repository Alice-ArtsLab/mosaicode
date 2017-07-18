from unittest import TestCase
from mosaicode.control.diagramcontrol import DiagramControl
from mosaicode.control.maincontrol import MainControl
from mosaicode.GUI.mainwindow import MainWindow


class TestDiagramControl(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        win = MainControl(MainWindow())
        self.diagram_control = DiagramControl(win)

    # ----------------------------------------------------------------------
    def test_get_generator(self):
        self.diagram_control.get_generator()

    # ----------------------------------------------------------------------
    def test_load(self):
        self.diagram_control.load()

    # ----------------------------------------------------------------------
    def test_save(self):
        self.diagram_control.save()

    # ----------------------------------------------------------------------
    def test_export_png(self):
        self.diagram_control.export_png()
