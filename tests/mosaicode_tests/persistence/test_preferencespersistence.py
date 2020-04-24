from tests.mosaicode_tests.test_base import TestBase
from mosaicode.utils.FileUtils import *
from mosaicode.GUI.comment import Comment
from mosaicode.control.diagramcontrol import DiagramControl
from mosaicode.persistence.diagrampersistence import DiagramPersistence


class PreferencesPersistenceTest(TestBase):

    def test_load(self):
        file_name = get_temp_file() + ".mscd"
        diagram_control = self.create_diagram_control()

        comment = Comment(diagram_control.diagram, None)
        comment.diagram.file_name = file_name
        diagram_control.add_comment(comment)

        DiagramPersistence.save(comment.diagram)
        result = DiagramPersistence.load(comment.diagram)

        os.remove(file_name)

        self.assertTrue(result, "Failed to load preferences")

    def test_save(self):
        file_name = get_temp_file() + ".mscd"
        diagram_control = self.create_diagram_control()

        comment = Comment(diagram_control.diagram, None)
        comment.diagram.file_name = file_name
        diagram_control.add_comment(comment)

        result = DiagramPersistence.save(comment.diagram)

        os.remove(file_name)

        self.assertTrue(result, "Failed to save preferences")

