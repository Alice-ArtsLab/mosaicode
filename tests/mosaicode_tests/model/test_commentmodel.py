from tests.mosaicode_tests.test_base import TestBase
from mosaicode.GUI.fieldtypes import * 
from mosaicode.model.commentmodel import CommentModel

class TestCommentModel(TestBase):

    def setUp(self):
        pass

    def test_new(self):
        comment = CommentModel()
        comment.set_properties({"text": "Novo Teste"})
        comment.set_properties({"Not here": "Novo Teste"})
        str(comment)

        comment.set_properties(None)
        str(comment)

        comment.properties = []
        str(comment)

        comment.properties = None
        str(comment)

        comment.properties = None
        comment.set_properties({"text": "Novo Teste"})
        str(comment)

        comment.properties = [{"test": "Test"}]
        str(comment)

        comment = CommentModel(comment)

