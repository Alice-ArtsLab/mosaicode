from unittest import TestCase
from mosaicode.control.diagramcontrol import DiagramControl
from mosaicode.GUI.mainwindow import MainWindow
from mosaicode.GUI.diagram import Diagram

class TestDiagramControl(TestCase):

    def setUp(self):
        """Do the test basic setup."""
        diagram = Diagram(MainWindow())
        self.diagram_control = DiagramControl(diagram)

    # ----------------------------------------------------------------------
    def test_get_code_template(self):
        #self.diagram_control.get_code_template()
        self.assertIsNotNone(self.diagram_control.get_code_template())

    # ----------------------------------------------------------------------
    def test_load(self):
        self.assertFalse(self.diagram_control.load("Teste"))
        self.assertFalse(self.diagram_control.load(None))

    # ----------------------------------------------------------------------
    def test_save(self):
        file_name = None
        self.assertIsNotNone(self.diagram_control.save(file_name))
        file_name = "None"
        self.assertIsNotNone(self.diagram_control.save(file_name))
        #file_name = -1
        #self.assertIsNotNone(self.diagram_control.save(file_name))

    # ----------------------------------------------------------------------
    def test_export_png(self):
        self.assertFalse(self.diagram_control.export_png(None))
        self.assertTrue(self.diagram_control.export_png("diagrama.png"))
        self.assertFalse(self.diagram_control.export_png("Teste.png"))
