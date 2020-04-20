from tests.test_base import TestBase
from mosaicode.model.diagrammodel import DiagramModel

class TestDiagramModel(TestBase):

    def test_init(self):
        model = DiagramModel()
        self.assertEqual("Untitled", model.patch_name)
