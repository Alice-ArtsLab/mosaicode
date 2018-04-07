import unittest
from abc import ABCMeta
from mosaicode.GUI.diagram import Diagram
from mosaicode.GUI.mainwindow import MainWindow
from mosaicode.control.diagramcontrol import DiagramControl


class TestBase(unittest.TestCase):
    __metaclass__ = ABCMeta

    def create_main_window(self):
        return MainWindow()

    def create_diagram(self):
        return Diagram(self.create_main_window())

    def create_diagram_control(self):
        diagram_control = DiagramControl(self.create_diagram())
        diagram_control.connectors = []
        diagram_control.language = "language"
        return diagram_control

