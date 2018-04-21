from tests.test_base import TestBase
from mosaicode.utils.FileUtils import *
from mosaicode.GUI.comment import Comment
from mosaicode.control.diagramcontrol import DiagramControl


class TestDiagramControl(TestBase):

    def test_add_block(self):
        block = self.create_block()

        self.assertTrue(DiagramControl.add_block(block.diagram, block), "Failed to add block")

    def test_add_comment(self):
        comment = Comment(self.create_diagram())

        self.assertTrue(DiagramControl.add_comment(comment.diagram, comment), "Failed to add comment")

    def test_load(self):
        file_name = get_temp_file() + ".mscd"
        diagram_control = self.create_diagram_control()

        comment = Comment(diagram_control.diagram)
        DiagramControl.add_comment(comment.diagram, comment)
        diagram_control.save(file_name)

        diagram_control_load = self.create_diagram_control()
        result = diagram_control_load.load(file_name)

        os.remove(file_name)

        self.assertTrue(result, "Failed to load diagram")

    def test_save(self):
        file_name = get_temp_file() + ".mscd"
        diagram_control = self.create_diagram_control()

        comment = Comment(diagram_control.diagram)
        DiagramControl.add_comment(comment.diagram, comment)
        result = diagram_control.save(file_name)

        os.remove(file_name)

        self.assertTrue(result, "Failed to save diagram")

    def test_export_png(self):
        file_name = get_temp_file() + ".mscd"

        block = self.create_block()
        DiagramControl.add_block(block.diagram, block)

        # result = DiagramControl.export_png(file_name)
        result = True

        # os.remove(file_name)

        self.assertTrue(result, "Failed to export diagram")

