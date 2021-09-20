from tests.mosaicode.test_base import TestBase
from mosaicode.model.diagrammodel import DiagramModel

class TestDiagramModel(TestBase):

    def test_init(self):
        model = DiagramModel()
        str(model)
        model.file_name = "/tmp/test.mscd"
        self.assertEqual("test", model.patch_name)
