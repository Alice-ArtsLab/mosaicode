from tests.test_base import TestBase
from mosaicode.GUI.block import Block
from mosaicode.GUI.comment import Comment
from mosaicode.model.blockmodel import BlockModel
from mosaicode.control.diagramcontrol import DiagramControl


class TestDiagramControl(TestBase):

    def test_add_block(self):
        diagram_control = self.create_diagram_control()

        block_model = BlockModel()
        block_model.maxIO = 2

        block = Block(diagram_control, block_model)
        block.language = "language"

        self.assertTrue(DiagramControl.add_block(diagram_control.diagram, block), "Failed to add block")

    def test_add_comment(self):
        comment = Comment(self.create_diagram())

        self.assertTrue(DiagramControl.add_comment(comment.diagram, comment), "Failed to add comment")

    def test_load(self):
        self.assertFalse(True)

    def test_save(self):
        self.assertFalse(True)

    def test_export_png(self):
        self.assertFalse(True)

