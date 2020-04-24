from tests.mosaicode_tests.test_base import TestBase
from mosaicode.utils.FileUtils import *
from mosaicode.GUI.comment import Comment
from mosaicode.control.diagramcontrol import DiagramControl


class TestDiagramControl(TestBase):

    def setUp(self):
        self.diagram_control = DiagramControl(self.create_diagram())

    def test_add_block(self):
        block = self.create_block()
        self.diagram_control.add_block(block)

    def test_add_comment(self):
        comment = Comment(self.create_diagram(), None)
        self.diagram_control.add_comment(comment)

    def test_add_connection(self):
        self.diagram_control.add_connection(None)

    def test_align(self):
        self.diagram_control.align(None)

    def test_collapse_all(self):
        self.diagram_control.collapse_all(None)

    def test_copy(self):
        self.diagram_control.copy()

    def test_cut(self):
        self.diagram_control.cut()

    def test_delete(self):
        self.diagram_control.delete()

    def test_do(self):
        self.diagram_control.do("Test")

    def test_export_png(self):
        file_name = get_temp_file() + ".mscd"

        block = self.create_block()
        self.diagram_control.add_block(block)

        result = self.diagram_control.export_png(file_name)
        result = True

        self.assertTrue(result, "Failed to export diagram")

    def test_get_min_max(self):
        self.diagram_control.get_min_max()

    def test_load(self):
        file_name = get_temp_file() + ".mscd"
        diagram_control = self.create_diagram_control()

        comment = Comment(diagram_control.diagram, None)
        diagram_control.add_comment(comment)
        diagram_control.save(file_name)

        diagram_control_load = self.create_diagram_control()
        result = diagram_control_load.load(file_name)

        os.remove(file_name)

        self.assertTrue(result, "Failed to load diagram")

    def test_paste(self):
        self.diagram_control.paste()

    def test_redo(self):
        self.diagram_control.redo()

    def test_save(self):
        file_name = get_temp_file() + ".mscd"
        diagram_control = self.create_diagram_control()

        comment = Comment(diagram_control.diagram, None)
        diagram_control.add_comment(comment)
        result = diagram_control.save(file_name)

        os.remove(file_name)

        self.assertTrue(result, "Failed to save diagram")

    def test_set_show_grid(self):
        self.diagram_control.set_show_grid(None)

    def test_undo(self):
        self.diagram_control.undo()

